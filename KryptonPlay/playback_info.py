import sqlite3
from pathlib import Path

from fastapi import Depends, HTTPException

from audio_fallback import _probe_audio
from playback_pipeline import decide_playback


def install_playback_info(app, get_current_user, database_path: Path) -> None:
    @app.get("/api/v1/media/{media_id}/playback-info", include_in_schema=False)
    def playback_info(media_id: int, user=Depends(get_current_user)):
        with sqlite3.connect(database_path) as connection:
            row = connection.execute("SELECT file_path FROM media_items WHERE id=?", (media_id,)).fetchone()
        if row is None:
            raise HTTPException(404, "Mídia não encontrada.")
        source = Path(row[0]).resolve()
        if not source.is_file():
            raise HTTPException(404, "Arquivo de mídia não encontrado.")
        try:
            probe = _probe_audio(source)
            decision = decide_playback(probe)
        except (OSError, RuntimeError, ValueError) as exc:
            raise HTTPException(500, f"Não foi possível analisar a mídia: {exc}") from exc
        return {
            "media_id": media_id,
            "profile": decision["profile"],
            "mode": decision["mode"],
            "reason": decision["reason"],
            "container": decision["container"],
            "format_names": decision["format_names"],
            "video_codec": decision["video_codec"],
            "audio_codec": decision["audio_codec"],
            "video_compatible": decision["video_compatible"],
            "audio_compatible": decision["audio_compatible"],
            "fallback_required": decision["fallback_required"],
            "duration_seconds": decision["duration_seconds"],
        }
