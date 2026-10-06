"""Panel serveri: API + yig'ilgan frontend (panel/dist). Bot bilan bir jarayonda ishlaydi."""

import contextlib
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from tgagent.panel import content_api
from tgagent.panel.api import Deps, router

log = logging.getLogger(__name__)

DIST = Path(__file__).resolve().parents[3] / "panel" / "dist"
NOT_BUILT = (
    "<h3>Panel hali yig'ilmagan</h3><p>Terminalda: <code>cd panel &amp;&amp; npm install &amp;&amp; npm run build</code>, "
    "keyin botni qayta ishga tushiring.</p>"
)


def create_app(deps: Deps, dist: Path = DIST) -> FastAPI:
    app = FastAPI(title="TG Agent Q panel", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.deps = deps
    app.include_router(router)
    app.include_router(content_api.router)

    if (dist / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    async def spa(path: str):
        # Frontend o'z sahifalarini o'zi boshqaradi — /api dan boshqa hamma yo'l index.html
        if path.startswith("api/"):
            return HTMLResponse("Not found", status_code=404)
        file = dist / path
        if path and file.is_file() and dist in file.resolve().parents:
            return FileResponse(file)
        index = dist / "index.html"
        return FileResponse(index) if index.is_file() else HTMLResponse(NOT_BUILT)

    return app


class _Server(uvicorn.Server):
    # Ctrl+C ni aiogram ushlaydi, keyin panelni o'zimiz to'xtatamiz
    @contextlib.contextmanager
    def capture_signals(self):
        yield


def make_server(app: FastAPI, host: str, port: int) -> uvicorn.Server:
    return _Server(uvicorn.Config(app, host=host, port=port, log_level="warning", access_log=False))


async def serve_panel(server: uvicorn.Server) -> None:
    """Panel ishga tushmasa (masalan port band) — bot baribir ishlashda davom etadi."""
    try:
        await server.serve()
    except SystemExit:
        log.error("Panel ishga tushmadi: %s:%s band bo'lishi mumkin (.env da PANEL_PORT ni o'zgartiring)",
                  server.config.host, server.config.port)
