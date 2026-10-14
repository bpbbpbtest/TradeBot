"""WebSocket client for Bitpin public market-data channels (Centrifugo).

Subscribes to the public order-book and matches channels for one symbol.
Public channels do not require a user token.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Awaitable, Callable

import centrifuge

logger = logging.getLogger(__name__)

BookHandler = Callable[[dict[str, Any]], Awaitable[None] | None]
MatchesHandler = Callable[[dict[str, Any]], Awaitable[None] | None]

_READY_TIMEOUT_SEC = 15.0


class _BookHandler(centrifuge.SubscriptionEventHandler):
    def __init__(self, callback: BookHandler) -> None:
        super().__init__()
        self._callback = callback

    async def on_publication(self, ctx: centrifuge.PublicationContext) -> None:
        data = ctx.pub.data
        if not isinstance(data, dict):
            logger.debug("Ignoring non-dict orderbook publication")
            return
        # Isolate: an exception here would otherwise kill the client's single
        # message pump and silently stop BOTH channels until a ping timeout.
        try:
            result = self._callback(data)
            if inspect.isawaitable(result):
                await result
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            logger.exception("orderbook callback failed; publication dropped")

    async def on_error(
        self, ctx: centrifuge.SubscriptionErrorContext
    ) -> None:
        logger.error("orderbook subscription error: %s", ctx)

    async def on_unsubscribed(self, ctx: centrifuge.UnsubscribedContext) -> None:
        logger.warning("orderbook subscription unsubscribed: %s", ctx)


class _MatchesHandler(centrifuge.SubscriptionEventHandler):
    def __init__(self, callback: MatchesHandler) -> None:
        super().__init__()
        self._callback = callback

    async def on_publication(self, ctx: centrifuge.PublicationContext) -> None:
        data = ctx.pub.data
        if not isinstance(data, dict):
            logger.debug("Ignoring non-dict matches publication")
            return
        try:
            result = self._callback(data)
            if inspect.isawaitable(result):
                await result
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            logger.exception("matches callback failed; publication dropped")

    async def on_error(
        self, ctx: centrifuge.SubscriptionErrorContext
    ) -> None:
        logger.error("matches subscription error: %s", ctx)

    async def on_unsubscribed(self, ctx: centrifuge.UnsubscribedContext) -> None:
        logger.warning("matches subscription unsubscribed: %s", ctx)


class _ClientHandler(centrifuge.ClientEventHandler):
    async def on_connected(self, ctx: centrifuge.ConnectedContext) -> None:
        logger.info("Centrifugo connection established")

    async def on_disconnected(self, ctx: centrifuge.DisconnectedContext) -> None:
        logger.warning(
            "Centrifugo connection lost (code=%s); client will auto-reconnect",
            getattr(ctx, "code", "?"),
        )

    async def on_error(self, ctx: centrifuge.ErrorContext) -> None:
        logger.error("Centrifugo error: %s", ctx)


class BitpinWsClient:
    """Maintains a Centrifugo connection and two public subscriptions."""

    def __init__(
        self,
        ws_url: str,
        symbol: str,
        on_book: BookHandler,
        on_matches: MatchesHandler,
    ) -> None:
        self._symbol = symbol
        self._client = centrifuge.Client(ws_url, events=_ClientHandler())
        self._book_sub = self._client.new_subscription(
            f"orderbook:{symbol}",
            events=_BookHandler(on_book),
        )
        self._matches_sub = self._client.new_subscription(
            f"matches:{symbol}",
            events=_MatchesHandler(on_matches),
        )

    async def start(self) -> None:
        await self._book_sub.subscribe()
        await self._matches_sub.subscribe()
        await self._client.connect()
        # connect() never raises on transport failure; wait for the actual
        # subscription confirmations so callers know the feed is live.
        await asyncio.gather(
            self._book_sub.ready(timeout=_READY_TIMEOUT_SEC),
            self._matches_sub.ready(timeout=_READY_TIMEOUT_SEC),
        )
        logger.info(
            "WebSocket connected; subscribed to orderbook:%s and matches:%s",
            self._symbol,
            self._symbol,
        )

    async def stop(self) -> None:
        await self._client.disconnect()
        logger.info("WebSocket disconnected")
