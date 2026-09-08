import os
import sys

import uvicorn


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import launcher


port = int(os.environ.get("KRYPTONPLAY_TEST_PORT", "18001"))
launcher.server_config["port"] = port

uvicorn.run(
    launcher.app,
    host="127.0.0.1",
    port=port,
    reload=False,
    log_config=None,
)
