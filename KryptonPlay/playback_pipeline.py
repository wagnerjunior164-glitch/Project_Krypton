import logging
import os
import sqlite3
import subprocess
import tempfile
from pathlib import Path

from fastapi import Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse

from audio_fallback import (
    FALLBACK_MIME_TYPE,
    _bundled_tool,
    _media_mime_type,
    _stream_cached_fallback,
    _stream_direct_fallback,
    _stream_progressive_fallback,
    prepare_playback_source,
)

logger = logging.getLogger("kryptonplay.playback")

WEB_VIDEO_CODECS = {"h264", "vp8", "vp9", "av1"}
WEB_AUDIO_CODECS = {"aac", "mp3", "opus", "vorbis"}
MP4_AUDIO_CODECS = {"aac", "mp3", "opus"}
WEBM_VIDEO_CODECS = {"vp8", "vp9", "av1"}
WEBM_AUDIO_CODECS = {"opus", "vorbis"}


def _format_names(probe: dict) -> set[str]:
    raw = str((probe.get("format") or {}).get("format_name") or "").lower()
    return {part.strip() for part in raw.split(",") if part.strip()}


def _default_stream(streams: list[dict], codec_type: str):
    candidates = [s for s in streams if s.get("codec_type") == codec_type]
    if not candidates:
        return None
    for stream in candidates:
        if stream.get("disposition", {}).get("default") == 1:
            return stream
    return candidates[0]


def decide_playback(probe: dict) -> dict:
    streams = probe.get("streams", [])
    video = _default_stream(streams, "video")
    audio = _default_stream(streams, "audio")
    video_codec = (video or {}).get("codec_name")
    audio_codec = (audio or {}).get("codec_name")
    formats = _format_names(probe)
    has_video = video is not None
    video_web_compatible = not has_video or video_codec in WEB_VIDEO_CODECS
    audio_web_compatible = audio is None or audio_codec in WEB_AUDIO_CODECS

    if "matroska" in formats and "webm" not in formats:
        container_family = "matroska"
    elif "webm" in formats:
        container_family = "webm"
    elif formats & {"mov", "mp4", "m4v", "3gp", "3g2", "mj2"}:
        container_family = "mp4"
    else:
        container_family = "other"

    direct_play = False
    if container_family == "mp4":
        direct_play = (
            (not has_video or video_codec in {"h264", "av1", "vp9"})
            and (audio is None or audio_codec in MP4_AUDIO_CODECS)
        )
    elif container_family == "webm":
        direct_play = (
            (not has_video or video_codec in WEBM_VIDEO_CODECS)
            and (audio is None or audio_codec in WEBM_AUDIO_CODECS)
        )

    if direct_play:
        mode = "direct-play"
        reason = "container_and_codecs_supported"
    elif video_web_compatible and audio_web_compatible:
        mode = "direct-stream"
        reason = "compatible_codecs_require_container_remux"
    else:
        mode = "transcoding"
        if video_web_compatible and not audio_web_compatible:
            reason = "audio_codec_incompatible"
        elif not video_web_compatible and audio_web_compatible:
            reason = "video_codec_incompatible"
        else:
            reason = "audio_and_video_codecs_incompatible"

    return {
        "profile": "web-chromium",
        "mode": mode,
        "reason": reason,
        "container": container_family,
        "format_names": sorted(formats),
        "video_codec": video_codec,
        "audio_codec": audio_codec,
        "video_stream_index": (video or {}).get("index"),
        "audio_stream_index": (audio or {}).get("index"),
        "fallback_required": mode != "direct-play",
        "video_compatible": video_web_compatible,
        "audio_compatible": audio_web_compatible,
        "duration_seconds": _duration_seconds(probe),
    }


def _duration_seconds(probe: dict):
    raw = (probe.get("format") or {}).get("duration")
    try:
        return float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def _stream_process(process, stderr_file, error_message):
    assert process.stdout is not None
    try:
        for chunk in iter(lambda: process.stdout.read(1024 * 1024), b""):
            yield chunk
    finally:
        process.stdout.close()
    returncode = process.wait()
    stderr_file.seek(0)
    stderr = stderr_file.read().decode("utf-8", errors="replace").strip()
    if returncode != 0:
        raise RuntimeError(stderr or error_message)


def _start_ffmpeg_stream(command: list[str]):
    stderr_file = tempfile.TemporaryFile(mode="w+b")
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=stderr_file,
        )
    except OSError:
        stderr_file.close()
        raise
    return process, stderr_file


def _stream_direct_stream(source: Path, media_id: int, start_seconds: float = 0.0):
    ffmpeg = _bundled_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg não está disponível no ambiente.")
    command = [ffmpeg, "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(source)]
    if start_seconds > 0:
        command += ["-ss", f"{start_seconds:.3f}"]
    command += [
        "-map", "0:v:0",
        "-map", "0:a:0?",
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "-f", "mp4",
        "pipe:1",
    ]
    process = stderr_file = None
    try:
        process, stderr_file = _start_ffmpeg_stream(command)
        logger.info(
            "direct_stream_process media_id=%s pid=%s start=%.3f container=mp4",
            media_id,
            process.pid,
            start_seconds,
        )
        yield from _stream_process(process, stderr_file, "FFmpeg não conseguiu remuxar a mídia para MP4.")
        logger.info("direct_stream_complete media_id=%s start=%.3f container=mp4", media_id, start_seconds)
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        if stderr_file is not None:
            stderr_file.close()


def _stream_full_transcode(source: Path, media_id: int, audio_stream_index: int | None, start_seconds: float = 0.0):
    ffmpeg = _bundled_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg não está disponível no ambiente.")
    command = [ffmpeg, "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(source)]
    if start_seconds > 0:
        command += ["-ss", f"{start_seconds:.3f}"]
    command += ["-map", "0:v:0"]
    if audio_stream_index is not None:
        command += ["-map", f"0:{audio_stream_index}", "-c:a", "aac", "-b:a", "192k"]
    command += [
        "-c:v", "libx264",
        "-preset", os.getenv("KRYPTONPLAY_TRANSCODE_PRESET", "veryfast"),
        "-crf", os.getenv("KRYPTONPLAY_TRANSCODE_CRF", "20"),
        "-pix_fmt", "yuv420p",
        "-avoid_negative_ts", "make_zero",
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "-f", "mp4",
        "pipe:1",
    ]
    process = stderr_file = None
    try:
        process, stderr_file = _start_ffmpeg_stream(command)
        logger.info(
            "transcoding_process media_id=%s pid=%s start=%.3f video=h264 audio=aac container=mp4",
            media_id,
            process.pid,
            start_seconds,
        )
        yield from _stream_process(process, stderr_file, "FFmpeg não conseguiu transcodificar a mídia.")
        logger.info(
            "transcoding_complete media_id=%s start=%.3f video=h264 audio=%s container=mp4",
            media_id,
            start_seconds,
            "aac" if audio_stream_index is not None else "none",
        )
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        if stderr_file is not None:
            stderr_file.close()


def install_playback_pipeline(app, get_current_user, database_path: Path, base_dir: Path) -> None:
    for route in list(app.router.routes):
        if getattr(route, "path", None) == "/api/v1/media/{media_id}/stream" and getattr(route, "methods", set()) == {"GET"}:
            app.router.routes.remove(route)

    @app.get("/api/v1/media/{media_id}/stream", include_in_schema=False)
    def stream_media(media_id: int, request: Request, user=Depends(get_current_user)):
        import audio_fallback

        range_header = request.headers.get("range")
        start_raw = request.query_params.get("start")
        try:
            start_seconds = max(0.0, float(start_raw)) if start_raw is not None else 0.0
        except ValueError as exc:
            raise HTTPException(400, "Parâmetro start inválido.") from exc

        with sqlite3.connect(database_path) as connection:
            row = connection.execute("SELECT file_path FROM media_items WHERE id=?", (media_id,)).fetchone()
        if row is None:
            raise HTTPException(404, "Mídia não encontrada.")
        source = Path(row[0]).resolve()
        if not source.is_file():
            raise HTTPException(404, "Arquivo de mídia não encontrado.")

        try:
            probe = audio_fallback._probe_audio(source)
            decision = decide_playback(probe)
        except (OSError, RuntimeError, ValueError):
            logger.exception("playback_decision_failed media_id=%s source=%s", media_id, source)
            raise HTTPException(500, "Falha ao analisar a mídia para decisão de reprodução.")

        logger.info(
            "playback_decision media_id=%s mode=%s reason=%s container=%s video=%s audio=%s range=%s start=%.3f",
            media_id,
            decision["mode"],
            decision["reason"],
            decision["container"],
            decision["video_codec"] or "none",
            decision["audio_codec"] or "none",
            range_header or "none",
            start_seconds,
        )

        if decision["mode"] == "direct-play":
            return FileResponse(source, media_type=_media_mime_type(source), content_disposition_type="inline")

        headers = {
            "Content-Disposition": "inline",
            "Accept-Ranges": "none",
            "Cache-Control": "no-store",
            "X-KryptonPlay-Playback-Mode": decision["mode"],
        }
        if range_header:
            logger.info(
                "playback_range_request media_id=%s mode=%s range=%s behavior=temporal_or_stream",
                media_id,
                decision["mode"],
                range_header,
            )

        if decision["mode"] == "direct-stream":
            body = _stream_direct_stream(source, media_id, start_seconds)
            return StreamingResponse(body, media_type=FALLBACK_MIME_TYPE, headers=headers)

        if decision["video_compatible"] and not decision["audio_compatible"]:
            _, fallback = prepare_playback_source(
                base_dir,
                media_id,
                source,
                allow_progressive_owner=start_seconds == 0,
            )
            cache = Path(fallback["cache_path"])
            if start_seconds > 0:
                if fallback.get("cache_pending") or not cache.is_file() or cache.stat().st_size == 0:
                    body = _stream_direct_fallback(source, media_id, fallback["source_stream_index"], start_seconds)
                else:
                    body = _stream_cached_fallback(source, cache, media_id, start_seconds)
            elif fallback.get("progressive_owner"):
                body = _stream_progressive_fallback(
                    source,
                    cache,
                    media_id,
                    fallback["source_stream_index"],
                    fallback["transcode_event"],
                )
            elif fallback.get("cache_pending"):
                body = _stream_direct_fallback(source, media_id, fallback["source_stream_index"])
            else:
                body = _stream_cached_fallback(source, cache, media_id)
            return StreamingResponse(body, media_type=FALLBACK_MIME_TYPE, headers=headers)

        body = _stream_full_transcode(source, media_id, decision["audio_stream_index"], start_seconds)
        return StreamingResponse(body, media_type=FALLBACK_MIME_TYPE, headers=headers)

    app.state.playback_pipeline_enabled = True
