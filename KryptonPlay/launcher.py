import ctypes
import ctypes.wintypes
import os, sqlite3, subprocess, sys, threading, time, webbrowser, atexit
from pathlib import Path
if getattr(sys,"frozen",False):
    bundle_dir=getattr(sys,"_MEIPASS",None)
    if bundle_dir:os.environ["PATH"]=str(bundle_dir)+os.pathsep+os.environ.get("PATH","")
import uvicorn
if os.name=="nt":
    _original_popen=subprocess.Popen;_ffmpeg_job=None
    try:
        _kernel32=ctypes.WinDLL("kernel32",use_last_error=True)
        _kernel32.CreateJobObjectW.argtypes=[ctypes.wintypes.LPVOID,ctypes.wintypes.LPCWSTR];_kernel32.CreateJobObjectW.restype=ctypes.wintypes.HANDLE
        _kernel32.SetInformationJobObject.argtypes=[ctypes.wintypes.HANDLE,ctypes.wintypes.DWORD,ctypes.wintypes.LPVOID,ctypes.wintypes.DWORD];_kernel32.SetInformationJobObject.restype=ctypes.wintypes.BOOL
        _kernel32.AssignProcessToJobObject.argtypes=[ctypes.wintypes.HANDLE,ctypes.wintypes.HANDLE];_kernel32.AssignProcessToJobObject.restype=ctypes.wintypes.BOOL
        class _J(ctypes.Structure):_fields_=[("PerProcessUserTimeLimit",ctypes.c_longlong),("PerJobUserTimeLimit",ctypes.c_longlong),("LimitFlags",ctypes.c_ulong),("MinimumWorkingSetSize",ctypes.c_size_t),("MaximumWorkingSetSize",ctypes.c_size_t),("ActiveProcessLimit",ctypes.c_ulong),("Affinity",ctypes.c_size_t),("PriorityClass",ctypes.c_ulong),("SchedulingClass",ctypes.c_ulong)]
        class _I(ctypes.Structure):_fields_=[("ReadOperationCount",ctypes.c_ulonglong),("WriteOperationCount",ctypes.c_ulonglong),("OtherOperationCount",ctypes.c_ulonglong),("ReadTransferCount",ctypes.c_ulonglong),("WriteTransferCount",ctypes.c_ulonglong),("OtherTransferCount",ctypes.c_ulonglong)]
        class _E(ctypes.Structure):_fields_=[("BasicLimitInformation",_J),("IoInfo",_I),("ProcessMemoryLimit",ctypes.c_size_t),("JobMemoryLimit",ctypes.c_size_t),("PeakProcessMemoryUsed",ctypes.c_size_t),("PeakJobProcessMemoryUsed",ctypes.c_size_t)]
        _ffmpeg_job=_kernel32.CreateJobObjectW(None,"KryptonPlay-FFmpeg")
        if _ffmpeg_job:
            limits=_E();limits.BasicLimitInformation.LimitFlags=0x2000
            if not _kernel32.SetInformationJobObject(_ffmpeg_job,9,ctypes.byref(limits),ctypes.sizeof(limits)):_ffmpeg_job=None
    except (AttributeError,OSError,TypeError):_ffmpeg_job=None
    def _hidden_console_popen(*args,**kwargs):
        kwargs.setdefault("creationflags",subprocess.CREATE_NO_WINDOW);p=_original_popen(*args,**kwargs)
        if _ffmpeg_job is not None:
            try:_kernel32.AssignProcessToJobObject(_ffmpeg_job,ctypes.wintypes.HANDLE(p._handle))
            except (AttributeError,OSError,TypeError):pass
        return p
    subprocess.Popen=_hidden_console_popen
else:_original_popen=subprocess.Popen
import app as app_module
from app import BASE_DIR,app,database_path,get_current_user,server_config
from audio_fallback import install_stream_fallback
from playback_info import install_playback_info
from playback_pipeline import install_playback_pipeline
from playback_ui import install_playback_ui
from update_api import install_update_api
from update_service import download_installer,latest_release
from mdns_service import LocalDiscovery
from version import VERSION
from kryptonplay_fixes import install as install_runtime_fixes
from increment24_hardening import install as install_increment24_hardening
from admin_features import install as install_admin_features
from ui_runtime import install as install_ui_runtime
app.version=VERSION
install_stream_fallback(app,get_current_user,database_path,BASE_DIR);install_playback_pipeline(app,get_current_user,database_path,BASE_DIR);install_playback_info(app,get_current_user,database_path);install_playback_ui(app);install_update_api(app);install_runtime_fixes(app_module);install_increment24_hardening(app_module);install_admin_features(app_module);install_ui_runtime(app_module)
def apply_saved_server_settings():
    try:
        with sqlite3.connect(database_path) as c:row=c.execute("SELECT value FROM server_settings WHERE key='network_access'").fetchone()
        access=row[0] if row else "local";server_config["host"]="0.0.0.0" if access=="lan" else "127.0.0.1"
    except sqlite3.Error:pass
apply_saved_server_settings()
local_discovery=LocalDiscovery()
def start_local_discovery():
    try:local_discovery.start(int(server_config["port"]),"lan" if server_config.get("host")=="0.0.0.0" else "local")
    except Exception:pass
def try_auto_update():
    if not getattr(sys,"frozen",False):return False
    try:
        with sqlite3.connect(database_path) as c:row=c.execute("SELECT value FROM server_settings WHERE key='auto_update_enabled'").fetchone()
        if row and str(row[0]).lower()!="true":return False
        r=latest_release()
        if not r["update_available"]:return False
        base=Path(sys.executable).resolve().parent;updater=base/"KryptonPlay-Updater.exe"
        if not updater.is_file():return False
        installer=download_installer();subprocess.Popen([str(updater),"--installer",str(installer),"--parent-pid",str(os.getpid()),"--app",str(Path(sys.executable).resolve())],cwd=str(base),creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0),close_fds=True);return True
    except Exception:return False
def open_browser():time.sleep(1.5);webbrowser.open("http://kryptonplay.local")
def _cleanup_runtime():
    local_discovery.close()
    if os.name=="nt" and _ffmpeg_job:
        try:_kernel32.CloseHandle(_ffmpeg_job)
        except (AttributeError,OSError,TypeError):pass
atexit.register(_cleanup_runtime)
if __name__=="__main__":
    restart_child="--restart-child" in sys.argv
    if not restart_child and try_auto_update():raise SystemExit(0)
    if restart_child:time.sleep(2)
    start_local_discovery();threading.Thread(target=open_browser,daemon=True).start();uvicorn.run(app,host=server_config["host"],port=server_config["port"],reload=False,log_config=None)
