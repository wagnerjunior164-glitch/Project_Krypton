"""HTTP endpoints for the KryptonPlay update flow."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from fastapi import APIRouter, Depends, HTTPException

from app import get_current_user
from update_service import download_installer, latest_release

router = APIRouter(prefix="/api/v1/update", tags=["updates"])


@router.get("/check")
def check_update():
    try:
        return latest_release()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Não foi possível verificar atualizações: {exc}") from exc


@router.post("/apply")
def apply_update(_user=Depends(get_current_user)):
    try:
        release = latest_release()
        if not release["update_available"]:
            return {"update_started": False, "current_version": release["current_version"], "latest_version": release["latest_version"]}

        base_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        updater = base_dir / "KryptonPlay-Updater.exe"
        if not updater.is_file():
            raise RuntimeError("O atualizador separado não está instalado.")

        installer = download_installer()
        app_exe = base_dir / "KryptonPlay.exe"
        if not app_exe.is_file():
            installer.unlink(missing_ok=True)
            raise RuntimeError("O executável principal do KryptonPlay não foi encontrado.")

        subprocess.Popen(
            [
                str(updater),
                "--installer", str(installer),
                "--parent-pid", str(os.getpid()),
                "--app", str(app_exe),
            ],
            cwd=str(base_dir),
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            close_fds=True,
        )
        return {
            "update_started": True,
            "current_version": release["current_version"],
            "latest_version": release["latest_version"],
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Não foi possível iniciar a atualização: {exc}") from exc


def install_update_api(app) -> None:
    app.include_router(router)
