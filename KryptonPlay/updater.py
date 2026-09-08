"""Standalone Windows updater for KryptonPlay.

The main process downloads and verifies the official installer. This process is
started separately so the KryptonPlay executable can exit before its files are
replaced. The updater waits for the parent process, runs Inno Setup silently,
and starts KryptonPlay again only after a successful installation.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time


def wait_for_process_exit(pid: int, timeout: int = 60) -> None:
    if pid <= 0:
        return
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            pass
        time.sleep(0.5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installer", required=True)
    parser.add_argument("--parent-pid", type=int, required=True)
    parser.add_argument("--app", required=True)
    args = parser.parse_args()

    installer = Path(args.installer).resolve()
    app = Path(args.app).resolve()
    if not installer.is_file():
        return 2
    if not app.is_file():
        return 3

    wait_for_process_exit(args.parent_pid)
    result = subprocess.run(
        [
            str(installer),
            "/VERYSILENT",
            "/SUPPRESSMSGBOXES",
            "/NORESTART",
            "/CLOSEAPPLICATIONS",
            "/RESTARTAPPLICATIONS",
        ],
        check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        installer.unlink(missing_ok=True)
    except OSError:
        pass

    if result.returncode != 0:
        return result.returncode

    subprocess.Popen(
        [str(app)],
        cwd=str(app.parent),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        close_fds=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
