import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from mimetypes import guess_type
from pathlib import Path

from fastapi import Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse

INCOMPATIBLE_AUDIO_CODECS = {"ac3", "dts", "dca"}
CACHE_DIR_NAME = "audio_fallback_cache"
AAC_BITRATE = "192k"
FALLBACK_MIME_TYPE = "video/mp4"
MEDIA_MIME_TYPES = {".mkv":"video/x-matroska",".mk3d":"video/x-matroska",".mp4":"video/mp4",".m4v":"video/mp4",".webm":"video/webm",".mov":"video/quicktime",".avi":"video/x-msvideo",".mpeg":"video/mpeg",".mpg":"video/mpeg",".ts":"video/mp2t"}
_transcode_state_lock = threading.Lock()
_active_transcodes = {}
logger = logging.getLogger("kryptonplay.playback")


def _configure_playback_logger(base_dir: Path) -> Path:
    log_path = base_dir / "data" / "playback.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    resolved = str(log_path.resolve()).casefold()
    if not any(isinstance(h, logging.FileHandler) and str(getattr(h,"baseFilename"," ")).casefold() == resolved for h in logger.handlers):
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True
    return log_path


def _media_mime_type(path: Path) -> str:
    return MEDIA_MIME_TYPES.get(path.suffix.lower()) or guess_type(path.name)[0] or "application/octet-stream"


def _cache_dir(base_dir: Path, source: Path) -> Path:
    if source.drive and base_dir.drive and source.drive.casefold() != base_dir.drive.casefold():
        return Path(source.drive + "\\") / "KryptonPlay" / "data" / CACHE_DIR_NAME
    return base_dir / "data" / CACHE_DIR_NAME


def _bundled_tool(name: str) -> str | None:
    executable = f"{name}.exe" if os.name == "nt" else name
    candidates = []
    configured = os.getenv(f"KRYPTONPLAY_{name.upper()}")
    if configured: candidates.append(Path(configured))
    if getattr(sys,"frozen",False):
        meipass = Path(getattr(sys,"_MEIPASS",Path(sys.executable).parent))
        candidates += [meipass/executable, meipass/"ffmpeg"/executable]
    path = shutil.which(name)
    if path: candidates.append(Path(path))
    return next((str(p) for p in candidates if p.is_file()),None)


def _probe_audio(file_path: Path) -> dict:
    ffprobe = _bundled_tool("ffprobe")
    if not ffprobe: raise RuntimeError("ffprobe não está disponível no ambiente.")
    try:
        completed = subprocess.run([ffprobe,"-v","error","-show_streams","-show_format","-of","json",str(file_path)],capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=30,check=False)
    except OSError as exc: raise RuntimeError(f"ffprobe não pôde ser executado: {exc}") from exc
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or f"processo retornou código {completed.returncode}"
        logger.error("ffprobe_failed source=%s returncode=%s detail=%s",file_path,completed.returncode,detail)
        raise RuntimeError(f"ffprobe não conseguiu analisar o arquivo: {detail}")
    try: return json.loads(completed.stdout or "{}")
    except json.JSONDecodeError as exc:
        logger.error("ffprobe_invalid_json source=%s stdout=%s",file_path,completed.stdout[:4000])
        raise RuntimeError("ffprobe retornou uma resposta JSON inválida.") from exc


def _default_audio_stream(streams: list[dict]):
    audio = [s for s in streams if s.get("codec_type")=="audio"]
    if not audio: return None
    for position,stream in enumerate(audio):
        if stream.get("disposition",{}).get("default")==1: return position,stream
    return 0,audio[0]


def classify_audio(file_path: Path) -> dict:
    selected = _default_audio_stream(_probe_audio(file_path).get("streams",[]))
    if selected is None:
        logger.info("audio_classification source=%s codec=none fallback=false",file_path)
        return {"audio_stream":None,"codec":None,"compatible":True,"fallback_required":False}
    position,stream = selected
    codec = (stream.get("codec_name") or "").lower()
    fallback = codec in INCOMPATIBLE_AUDIO_CODECS
    result = {"audio_stream":position,"source_stream_index":stream.get("index"),"codec":codec,"compatible":not fallback,"fallback_required":fallback}
    logger.info("audio_classification source=%s audio_position=%s source_stream=%s codec=%s fallback=%s",file_path,position,stream.get("index"),codec or "unknown",fallback)
    return result


def _cache_path(base_dir: Path, media_id: int, audio_position: int, source: Path) -> Path:
    fingerprint = f"{source.resolve()}|{source.stat().st_size}|{source.stat().st_mtime_ns}|{audio_position}"
    digest = hashlib.sha256(fingerprint.encode()).hexdigest()[:16]
    cache_dir = _cache_dir(base_dir,source)
    cache_dir.mkdir(parents=True,exist_ok=True)
    return cache_dir / f"media-{media_id}-audio-{audio_position}-{digest}.m4a"


def _remove_stale_caches(base_dir: Path, media_id: int, keep: Path, source: Path) -> None:
    cache_dir = _cache_dir(base_dir,source)
    if not cache_dir.exists(): return
    for pattern in (f"media-{media_id}-audio-*.m4a",f"media-{media_id}-audio-*.partial.aac"):
        for candidate in cache_dir.glob(pattern):
            if candidate == keep: continue
            try: candidate.unlink(); logger.info("cache_removed media_id=%s path=%s reason=stale",media_id,candidate)
            except OSError as exc: logger.warning("cache_remove_failed media_id=%s path=%s error=%s",media_id,candidate,exc)


def _remux_audio_cache(partial: Path,destination: Path) -> None:
    ffmpeg = _bundled_tool("ffmpeg")
    if not ffmpeg: raise RuntimeError("ffmpeg não está disponível no ambiente.")
    temporary = destination.with_suffix(".partial.m4a")
    if temporary.exists(): temporary.unlink()
    command=[ffmpeg,"-hide_banner","-nostdin","-loglevel","error","-y","-f","aac","-i",str(partial),"-c:a","copy","-f","ipod",str(temporary)]
    try:
        with tempfile.TemporaryFile(mode="w+b") as stderr_file:
            process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=stderr_file)
            returncode=process.wait(); stderr_file.seek(0); stderr=stderr_file.read().decode("utf-8",errors="replace").strip()
    except OSError as exc: raise RuntimeError(f"FFmpeg não pôde finalizar o cache de áudio: {exc}") from exc
    if returncode != 0 or not temporary.is_file() or temporary.stat().st_size==0:
        if temporary.exists(): temporary.unlink()
        raise RuntimeError(stderr or "FFmpeg não conseguiu finalizar o cache de áudio.")
    temporary.replace(destination)


def _start_audio_cache_process(source:Path,partial:Path,source_stream_index:int,media_id:int):
    ffmpeg=_bundled_tool("ffmpeg")
    if not ffmpeg: raise RuntimeError("ffmpeg não está disponível no ambiente.")
    if partial.exists(): partial.unlink()
    command=[ffmpeg,"-hide_banner","-nostdin","-loglevel","error","-y","-i",str(source),"-map",f"0:{source_stream_index}","-vn","-sn","-dn","-c:a","aac","-b:a",AAC_BITRATE,"-f","adts",str(partial)]
    stderr_file=tempfile.TemporaryFile(mode="w+b")
    try: process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=stderr_file)
    except OSError:
        stderr_file.close(); raise
    logger.info("fallback_audio_cache_process media_id=%s pid=%s partial=%s",media_id,process.pid,partial)
    return process,stderr_file


def _start_stream_process(source:Path,media_id:int,source_stream_index:int,start_seconds:float=0.0):
    ffmpeg=_bundled_tool("ffmpeg")
    if not ffmpeg: raise RuntimeError("ffmpeg não está disponível no ambiente.")
    command=[ffmpeg,"-hide_banner","-nostdin","-loglevel","error"]
    if start_seconds>0: command += ["-ss",f"{start_seconds:.3f}"]
    command += ["-i",str(source),"-map","0:v:0","-map",f"0:{source_stream_index}","-c:v","copy","-c:a","aac","-b:a",AAC_BITRATE,"-movflags","frag_keyframe+empty_moov+default_base_moof","-f","mp4","pipe:1"]
    stderr_file=tempfile.TemporaryFile(mode="w+b")
    try: process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=stderr_file)
    except OSError:
        stderr_file.close(); raise
    logger.info("fallback_playback_process media_id=%s pid=%s start=%.3f container=mp4",media_id,process.pid,start_seconds)
    return process,stderr_file


def _stream_process(process,stderr_file,error_message):
    assert process.stdout is not None
    try:
        for chunk in iter(lambda:process.stdout.read(1024*1024),b""): yield chunk
    finally:
        process.stdout.close()
    returncode=process.wait(); stderr_file.seek(0); stderr=stderr_file.read().decode("utf-8",errors="replace").strip()
    if returncode != 0: raise RuntimeError(stderr or error_message)


def _prepare_state(base_dir:Path,media_id:int,source:Path,diagnosis:dict,allow_owner:bool):
    cache=_cache_path(base_dir,media_id,diagnosis["audio_stream"],source)
    if cache.is_file() and cache.stat().st_size>0: return cache,False,False,None
    key=str(cache.resolve()).casefold()
    with _transcode_state_lock:
        state=_active_transcodes.get(key)
        if state is None and allow_owner:
            event=threading.Event(); _active_transcodes[key]={"event":event,"cache":cache}
            return cache,True,False,event
        if state is not None: return cache,False,True,state["event"]
        return cache,False,True,None


def prepare_playback_source(base_dir:Path,media_id:int,source:Path,allow_progressive_owner:bool=True):
    diagnosis=classify_audio(source)
    if not diagnosis["fallback_required"]:
        logger.info("playback_source media_id=%s source=%s fallback=false",media_id,source)
        return source,{**diagnosis,"fallback_used":False,"cache":False}
    cache,owner,pending,event=_prepare_state(base_dir,media_id,source,diagnosis,allow_progressive_owner)
    cache_hit=cache.is_file() and cache.stat().st_size>0
    if cache_hit: owner=pending=False; logger.info("fallback_cache_hit media_id=%s path=%s size=%s",media_id,cache,cache.stat().st_size)
    else: logger.info("fallback_cache_%s media_id=%s path=%s","miss" if owner else "pending",media_id,cache)
    return None,{**diagnosis,"fallback_used":True,"cache":True,"cache_hit":cache_hit,"cache_path":str(cache),"source_path":str(source),"progressive_owner":owner,"cache_pending":pending,"transcode_event":event}


def _stream_progressive_fallback(source:Path,cache:Path,media_id:int,source_stream_index:int,event:threading.Event):
    partial=cache.with_suffix(".partial.aac")
    playback=playback_err=cache_proc=cache_err=None
    started=time.monotonic()
    try:
        playback,playback_err=_start_stream_process(source,media_id,source_stream_index)
        cache_proc,cache_err=_start_audio_cache_process(source,partial,source_stream_index,media_id)
        yield from _stream_process(playback,playback_err,"FFmpeg não conseguiu gerar o stream progressivo.")
        cache_rc=cache_proc.wait(); cache_err.seek(0); cache_message=cache_err.read().decode("utf-8",errors="replace").strip()
        if cache_rc!=0: raise RuntimeError(cache_message or "FFmpeg não conseguiu gerar o cache AAC.")
        if not partial.is_file() or partial.stat().st_size==0: raise RuntimeError("FFmpeg não gerou áudio AAC progressivo válido.")
        _remux_audio_cache(partial,cache)
        logger.info("fallback_progressive_complete media_id=%s source=%s cache=%s elapsed=%.2fs cache_size=%s container=mp4",media_id,source,cache,time.monotonic()-started,cache.stat().st_size)
    except (OSError,RuntimeError) as exc:
        logger.error("fallback_progressive_failed media_id=%s source=%s elapsed=%.2fs error=%s",media_id,source,time.monotonic()-started,exc); raise
    finally:
        for process in (playback,cache_proc):
            if process is not None and process.poll() is None: process.kill(); process.wait()
        for handle in (playback_err,cache_err):
            if handle is not None: handle.close()
        if partial.exists():
            try: partial.unlink()
            except OSError: pass
        with _transcode_state_lock:
            _active_transcodes.pop(str(cache.resolve()).casefold(),None); event.set()


def _stream_direct_fallback(source:Path,media_id:int,source_stream_index:int,start_seconds:float=0.0):
    process=stderr_file=None
    try:
        process,stderr_file=_start_stream_process(source,media_id,source_stream_index,start_seconds)
        yield from _stream_process(process,stderr_file,"FFmpeg não conseguiu gerar o fallback.")
    finally:
        if process is not None and process.poll() is None: process.kill(); process.wait()
        if stderr_file is not None: stderr_file.close()


def _stream_cached_fallback(source:Path,audio_cache:Path,media_id:int,start_seconds:float=0.0):
    ffmpeg=_bundled_tool("ffmpeg")
    if not ffmpeg: raise RuntimeError("ffmpeg não está disponível no ambiente.")
    command=[ffmpeg,"-hide_banner","-nostdin","-loglevel","error"]
    if start_seconds>0: command += ["-ss",f"{start_seconds:.3f}"]
    command += ["-i",str(source)]
    if start_seconds>0: command += ["-ss",f"{start_seconds:.3f}"]
    command += ["-i",str(audio_cache),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy","-shortest","-movflags","frag_keyframe+empty_moov+default_base_moof","-f","mp4","pipe:1"]
    process=stderr_file=None; started=time.monotonic()
    try:
        stderr_file=tempfile.TemporaryFile(mode="w+b")
        process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=stderr_file)
        yield from _stream_process(process,stderr_file,"FFmpeg não conseguiu combinar vídeo e áudio.")
        logger.info("fallback_mux_complete media_id=%s source=%s audio_cache=%s start=%.3f elapsed=%.2fs container=mp4",media_id,source,audio_cache,start_seconds,time.monotonic()-started)
    finally:
        if process is not None and process.poll() is None: process.kill(); process.wait()
        if stderr_file is not None: stderr_file.close()


def install_stream_fallback(app,get_current_user,database_path:Path,base_dir:Path)->None:
    playback_log_path=_configure_playback_logger(base_dir); logger.info("playback_service_start log=%s",playback_log_path)
    for route in list(app.router.routes):
        if getattr(route,"path",None)=="/api/v1/media/{media_id}/stream" and getattr(route,"methods",set())=={"GET"}: app.router.routes.remove(route)
    @app.get("/api/v1/media/{media_id}/stream",include_in_schema=False)
    def stream_media_with_audio_fallback(media_id:int,request:Request,user=Depends(get_current_user)):
        import sqlite3
        range_header=request.headers.get("range"); start_raw=request.query_params.get("start")
        try: start_seconds=max(0.0,float(start_raw)) if start_raw is not None else 0.0
        except ValueError as exc: raise HTTPException(400,"Parâmetro start inválido.") from exc
        logger.info("stream_request media_id=%s user=%s range=%s start=%.3f user_agent=%s",media_id,user.get("username","unknown"),range_header or "none",start_seconds,request.headers.get("user-agent","unknown"))
        with sqlite3.connect(database_path) as connection: row=connection.execute("SELECT file_path FROM media_items WHERE id=?",(media_id,)).fetchone()
        if row is None: raise HTTPException(404,"Mídia não encontrada.")
        source=Path(row[0]).resolve()
        if not source.is_file(): raise HTTPException(404,"Arquivo de mídia não encontrado.")
        try: playback_source,diagnosis=prepare_playback_source(base_dir,media_id,source,allow_progressive_owner=start_seconds==0)
        except (OSError,RuntimeError,ValueError,json.JSONDecodeError) as exc:
            logger.exception("stream_prepare_failed media_id=%s source=%s",media_id,source); raise HTTPException(500,f"Falha ao preparar áudio compatível: {exc}") from exc
        if diagnosis["fallback_used"]:
            cache=Path(diagnosis["cache_path"]); headers={"Content-Disposition":"inline","Accept-Ranges":"none","Cache-Control":"no-store"}
            if range_header: logger.info("fallback_range_request media_id=%s range=%s behavior=progressive_stream_no_byte_range",media_id,range_header)
            if start_seconds>0:
                if diagnosis.get("cache_pending") or not cache.is_file() or cache.stat().st_size==0:
                    logger.info("fallback_seek_during_transcode media_id=%s start=%.3f cache_pending=%s",media_id,start_seconds,diagnosis.get("cache_pending"))
                    body=_stream_direct_fallback(source,media_id,diagnosis["source_stream_index"],start_seconds)
                else:
                    body=_stream_cached_fallback(source,cache,media_id,start_seconds)
            elif diagnosis.get("progressive_owner"):
                body=_stream_progressive_fallback(source,cache,media_id,diagnosis["source_stream_index"],diagnosis["transcode_event"])
            elif diagnosis.get("cache_pending"):
                body=_stream_direct_fallback(source,media_id,diagnosis["source_stream_index"])
            else:
                body=_stream_cached_fallback(source,cache,media_id)
            return StreamingResponse(body,media_type=FALLBACK_MIME_TYPE,headers=headers)
        assert playback_source is not None
        return FileResponse(playback_source,media_type=_media_mime_type(playback_source),content_disposition_type="inline")
    app.state.audio_fallback_enabled=True; app.state.playback_log_path=playback_log_path
