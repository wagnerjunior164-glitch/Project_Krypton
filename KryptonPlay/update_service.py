"""GitHub Release update service for KryptonPlay.

The service only reports and downloads official GitHub Releases. Installation is
left to the Inno Setup installer so program files and user data remain separate.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import urllib.request
from pathlib import Path

from version import VERSION

REPOSITORY = os.getenv("KRYPTONPLAY_UPDATE_REPOSITORY", "wagnerjunior164-glitch/Project_Krypton")
API_URL = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
ASSET_NAME = "KryptonPlay-Windows-Setup.exe"


def _version_tuple(value: str) -> tuple[int, int, int]:
    normalized = value.strip().lstrip("v").split("-", 1)[0]
    parts = normalized.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"Versão inválida: {value}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def latest_release() -> dict:
    request = urllib.request.Request(
        API_URL,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "KryptonPlay-Updater"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.load(response)
    tag = str(payload.get("tag_name", ""))
    remote_version = tag.lstrip("v")
    asset = next((item for item in payload.get("assets", []) if item.get("name") == ASSET_NAME), None)
    digest = asset.get("digest") if asset else None
    return {
        "current_version": VERSION,
        "latest_version": remote_version,
        "update_available": _version_tuple(remote_version) > _version_tuple(VERSION),
        "release_url": payload.get("html_url"),
        "release_name": payload.get("name") or f"KryptonPlay v{remote_version}",
        "release_notes": payload.get("body") or "",
        "published_at": payload.get("published_at"),
        "installer": {
            "name": ASSET_NAME,
            "download_url": asset.get("browser_download_url"),
            "digest": digest,
            "integrity_available": bool(digest and str(digest).startswith("sha256:") and len(str(digest).split(":", 1)[1]) == 64),
        } if asset else None,
    }


def download_installer(destination: Path | None = None) -> Path:
    release = latest_release()
    installer = release.get("installer") or {}
    url = installer.get("download_url")
    digest = str(installer.get("digest") or "")
    if not release["update_available"] or not url:
        raise RuntimeError("Nenhuma atualização instalável está disponível.")
    if not digest.startswith("sha256:") or len(digest.split(":", 1)[1]) != 64:
        raise RuntimeError("A Release não fornece um SHA-256 válido para o instalador.")
    if destination is None:
        fd, name = tempfile.mkstemp(prefix="KryptonPlay-Update-", suffix=".exe")
        os.close(fd)
        destination = Path(name)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, destination)
        expected = digest.split(":", 1)[1].lower()
        actual = hashlib.sha256(destination.read_bytes()).hexdigest().lower()
        if actual != expected:
            raise RuntimeError("A verificação SHA-256 do instalador falhou.")
        return destination
    except Exception:
        destination.unlink(missing_ok=True)
        raise
