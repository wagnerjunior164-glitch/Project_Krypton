from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class PlaybackUIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Playback controls and fallback seeking are implemented directly by
        # static/player.html. Keep this middleware as a compatibility layer for
        # older generated pages without injecting a second seek controller.
        response = await call_next(request)
        if request.url.path != "/" or "text/html" not in response.headers.get("content-type", ""):
            return response
        return response


def install_playback_ui(app) -> None:
    app.add_middleware(PlaybackUIMiddleware)
