"""Minimal local HTTP + SSE server for the live dashboard (stdlib only)."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from tradebot.dashboard.state import DashboardState

logger = logging.getLogger(__name__)

_STATIC_DIR = Path(__file__).parent / "static"
_SSE_INTERVAL_SEC = 0.8


class DashboardServer:
    """Serves the dashboard page and pushes live state over SSE.

    ``controller`` must provide:
      * async start_trading(symbol: str | None = None) -> dict
      * async stop_trading() -> dict
      * def status() -> dict
      * async symbols() -> list[str]
    """

    def __init__(
        self,
        state: DashboardState,
        host: str = "127.0.0.1",
        port: int = 8765,
        controller: Any = None,
    ) -> None:
        self._state = state
        self._host = host
        self._port = port
        self._controller = controller
        self._server: asyncio.Server | None = None
        self._index_html: bytes = b""

    @property
    def state(self) -> DashboardState:
        return self._state

    async def start(self) -> None:
        self._index_html = (_STATIC_DIR / "index.html").read_bytes()
        self._server = await asyncio.start_server(
            self._handle, self._host, self._port
        )
        logger.info("Dashboard: http://%s:%d", self._host, self._port)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:  # noqa: BLE001
                logger.debug("Dashboard server close failed", exc_info=True)
            self._server = None

    # ------------------------------------------------------------------
    # Request handling
    # ------------------------------------------------------------------

    async def _handle(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            request_line = await asyncio.wait_for(reader.readline(), timeout=10)
            parts = request_line.decode("latin-1", errors="replace").split()
            if len(parts) < 2:
                return
            method = parts[0].upper()
            path = parts[1].split("?", 1)[0]

            content_length = 0
            while True:
                line = await asyncio.wait_for(reader.readline(), timeout=10)
                if line in (b"\r\n", b"\n", b""):
                    break
                if line.lower().startswith(b"content-length:"):
                    try:
                        content_length = int(line.split(b":", 1)[1].strip())
                    except ValueError:
                        content_length = 0

            body = b""
            if content_length > 0:
                body = await asyncio.wait_for(
                    reader.readexactly(content_length), timeout=10
                )

            if method == "GET" and path in ("/", "/index.html"):
                await self._send_bytes(
                    writer, self._index_html, "text/html; charset=utf-8"
                )
            elif method == "GET" and path == "/api/state":
                await self._send_json(writer, self._state.tick())
            elif method == "GET" and path == "/api/history":
                await self._send_json(writer, {"history": self._state.history()})
            elif method == "GET" and path == "/api/symbols":
                await self._handle_symbols(writer)
            elif method == "POST" and path == "/api/control/start":
                await self._handle_start(writer, body)
            elif method == "POST" and path == "/api/control/stop":
                await self._handle_stop(writer)
            elif method == "GET" and path == "/events":
                await self._sse_loop(writer)
                return
            else:
                await self._send_bytes(
                    writer, b"Not found", "text/plain; charset=utf-8", status=404
                )
        except (asyncio.TimeoutError, ConnectionResetError, BrokenPipeError):
            pass
        except Exception:  # noqa: BLE001
            logger.debug("Dashboard request failed", exc_info=True)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:  # noqa: BLE001
                pass

    async def _handle_symbols(self, writer: asyncio.StreamWriter) -> None:
        if self._controller is None:
            await self._send_json(writer, {"symbols": []})
            return
        try:
            symbols = await self._controller.symbols()
            await self._send_json(writer, {"symbols": symbols})
        except Exception as exc:  # noqa: BLE001
            await self._send_json(writer, {"symbols": [], "error": str(exc)})

    async def _handle_start(
        self, writer: asyncio.StreamWriter, body: bytes
    ) -> None:
        payload: dict[str, Any] = {}
        if body:
            try:
                parsed = json.loads(body)
                if isinstance(parsed, dict):
                    payload = parsed
            except json.JSONDecodeError:
                pass
        symbol = payload.get("symbol")
        if self._controller is None:
            await self._send_json(
                writer, {"ok": False, "error": "no controller"}
            )
            return
        try:
            status = await self._controller.start_trading(symbol)
            await self._send_json(writer, {"ok": True, "status": status})
        except Exception as exc:  # noqa: BLE001
            status = self._controller.status()
            self._state.set_status(
                status.get("running", False),
                status.get("symbol", ""),
                str(exc),
            )
            await self._send_json(
                writer, {"ok": False, "error": str(exc), "status": status}
            )

    async def _handle_stop(self, writer: asyncio.StreamWriter) -> None:
        if self._controller is None:
            await self._send_json(
                writer, {"ok": False, "error": "no controller"}
            )
            return
        try:
            status = await self._controller.stop_trading()
            await self._send_json(writer, {"ok": True, "status": status})
        except Exception as exc:  # noqa: BLE001
            await self._send_json(writer, {"ok": False, "error": str(exc)})

    async def _sse_loop(self, writer: asyncio.StreamWriter) -> None:
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/event-stream\r\n"
            "Cache-Control: no-cache\r\n"
            "Connection: keep-alive\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "\r\n"
        )
        writer.write(headers.encode("latin-1"))
        await writer.drain()
        while True:
            payload = json.dumps(self._state.tick(), default=str)
            writer.write(f"data: {payload}\n\n".encode("utf-8"))
            await writer.drain()
            await asyncio.sleep(_SSE_INTERVAL_SEC)

    @staticmethod
    async def _send_bytes(
        writer: asyncio.StreamWriter,
        body: bytes,
        content_type: str,
        status: int = 200,
    ) -> None:
        reason = "OK" if status == 200 else "Not Found"
        headers = (
            f"HTTP/1.1 {status} {reason}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Cache-Control: no-cache\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        writer.write(headers.encode("latin-1") + body)
        await writer.drain()

    @classmethod
    async def _send_json(
        cls, writer: asyncio.StreamWriter, payload: Any
    ) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        await cls._send_bytes(writer, body, "application/json; charset=utf-8")
