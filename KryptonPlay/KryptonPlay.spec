from pathlib import Path
import os
import shutil

ROOT = Path(SPECPATH)
VENDOR_FFMPEG = ROOT / "vendor" / "ffmpeg"


def _choco_tools_dir() -> Path | None:
    candidates = [
        Path(r"C:\ProgramData\chocolatey\lib\ffmpeg\tools"),
        Path(os.getenv("ChocolateyInstall", r"C:\ProgramData\chocolatey")) / "lib" / "ffmpeg" / "tools",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def resolve_tool(name: str) -> str:
    executable = f"{name}.exe" if os.name == "nt" else name

    configured = os.getenv(f"KRYPTONPLAY_{name.upper()}")
    if configured and Path(configured).is_file():
        return str(Path(configured).resolve())

    bundled = VENDOR_FFMPEG / executable
    if bundled.is_file():
        return str(bundled.resolve())

    discovered = shutil.which(name)
    if discovered:
        discovered_path = Path(discovered).resolve()
        if os.name == "nt" and discovered_path.parent.name.lower() == "bin":
            tools_dir = _choco_tools_dir()
            if tools_dir:
                matches = sorted(tools_dir.rglob(executable))
                if matches:
                    return str(matches[0].resolve())
        return str(discovered_path)

    if os.name == "nt":
        tools_dir = _choco_tools_dir()
        if tools_dir:
            matches = sorted(tools_dir.rglob(executable))
            if matches:
                return str(matches[0].resolve())

    raise RuntimeError(f"{name} é obrigatório para o build do KryptonPlay.")


ffmpeg = resolve_tool("ffmpeg")
ffprobe = resolve_tool("ffprobe")
ffmpeg_path = Path(ffmpeg).resolve()
ffprobe_path = Path(ffprobe).resolve()
ffmpeg_dir = ffmpeg_path.parent
ffprobe_dir = ffprobe_path.parent

if os.name == "nt" and ffmpeg_dir != ffprobe_dir:
    raise RuntimeError(
        f"FFmpeg e FFprobe precisam estar no mesmo diretório de runtime: "
        f"{ffmpeg_dir} != {ffprobe_dir}."
    )

# FFmpeg 9 Windows builds may be self-contained and ship no DLL files beside
# the executables. When DLLs are present, include them; when they are absent,
# PyInstaller still receives ffmpeg.exe/ffprobe.exe as binaries and can analyze
# their native dependencies. The absence of side-by-side DLLs must not make a
# valid static FFmpeg build fail.
ffmpeg_runtime_dir = ffmpeg_dir
ffmpeg_dlls = sorted(
    path for path in ffmpeg_runtime_dir.rglob("*")
    if path.is_file() and path.suffix.lower() == ".dll"
)

binaries = [
    (str(ffmpeg_path), "."),
    (str(ffprobe_path), "."),
]
binaries.extend((str(dll), ".") for dll in ffmpeg_dlls)


a = Analysis(
    [str(ROOT / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=[
        (str(ROOT / "config"), "config"),
        (str(ROOT / "static"), "static"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="KryptonPlay",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    # The application itself requests elevation when launched. This is
    # intentionally independent from the install location configured by the
    # Inno Setup installer.
    uac_admin=True,
)
