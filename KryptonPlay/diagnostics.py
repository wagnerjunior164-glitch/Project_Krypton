import json
import shutil
import subprocess
from pathlib import Path


def probe_media(file_path: Path) -> dict:
    """Collect playback-relevant media metadata with ffprobe when available."""
    resolved = file_path.resolve()
    result = {
        "file": str(resolved),
        "exists": resolved.is_file(),
        "ffprobe": shutil.which("ffprobe") is not None,
        "container": None,
        "duration_seconds": None,
        "video": [],
        "audio": [],
        "subtitles": [],
        "error": None,
    }

    if not resolved.is_file():
        result["error"] = "Arquivo de mídia não encontrado."
        return result

    if not result["ffprobe"]:
        result["error"] = "ffprobe não está disponível no ambiente."
        return result

    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=format_name,duration:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,channels,channel_layout,sample_rate,language,title,disposition:stream_tags=language,title",
        "-of", "json", str(resolved),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        result["error"] = f"Falha ao executar ffprobe: {exc}"
        return result

    if completed.returncode != 0:
        result["error"] = completed.stderr.strip() or "ffprobe não conseguiu analisar o arquivo."
        return result

    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError as exc:
        result["error"] = f"Resposta inválida do ffprobe: {exc}"
        return result

    format_info = payload.get("format", {})
    result["container"] = format_info.get("format_name")
    duration = format_info.get("duration")
    try:
        result["duration_seconds"] = float(duration) if duration is not None else None
    except (TypeError, ValueError):
        result["duration_seconds"] = None

    for stream in payload.get("streams", []):
        item = {
            "index": stream.get("index"),
            "codec": stream.get("codec_name"),
            "profile": stream.get("profile"),
            "language": stream.get("tags", {}).get("language") or stream.get("language"),
            "title": stream.get("tags", {}).get("title") or stream.get("title"),
        }
        if stream.get("codec_type") == "video":
            item.update({"width": stream.get("width"), "height": stream.get("height"), "pixel_format": stream.get("pix_fmt")})
            result["video"].append(item)
        elif stream.get("codec_type") == "audio":
            item.update({"channels": stream.get("channels"), "channel_layout": stream.get("channel_layout"), "sample_rate": stream.get("sample_rate")})
            result["audio"].append(item)
        elif stream.get("codec_type") == "subtitle":
            result["subtitles"].append(item)

    return result


def playback_mode_diagnosis(media_info: dict) -> dict:
    """Describe the current KryptonPlay server behavior without changing playback."""
    return {
        "mode": "direct-play",
        "source": "original-media-file",
        "transcoding": False,
        "transcoding_reason": None,
        "diagnostic": media_info,
    }
