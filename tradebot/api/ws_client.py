"""WebSocket client for Bitpin public market-data channels (Centrifugo).

Subscribes to the public order-book and matches channels for one symbol.
Public channels do not require a user token.
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

import centrifuge

logger = logging.getLogger(__name__)

BookHandler = Callable[[dict[str, Any]], Awaitable[None] | None]
MatchesHandler = Callable[[dict[str, Any]], Awaitable[None] | None]


class _BookHandler(centrifuge.SubscriptionEventHandler):
    def __init__(self, callback: BookHandler) -> None:
        super().__init__()
        self._callback = callback

    async def on_publication(self, ctx: centrifuge.PublicationContext) -> None:
        data = ctx.pub.data
        if not isinstance(data, dict):
            logger.debug("Ignoring non-dict orderbook publication")
            return
        result = self._callback(data)
        if hasattr(result, "__await__"):
            await result


class _MatchesHandler(centrifuge.SubscriptionEventHandler):
    def __init__(self, callback: MatchesHandler) -> None:
        super().__init__()
        self._callback = callback

    async def on_publication(self, ctx: centrifuge.PublicationContext) -> None:
        data = ctx.pub.data
        if not isinstance(data, dict):
            logger.debug("Ignoring non-dict matches publication")
            return
        result = self._callback(data)
        if hasattr(result, "__await__"):
            await result


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
        logger.info(
            "WebSocket connected; subscribed to orderbook:%s and matches:%s",
            self._symbol,
            self._symbol,
        )

    async def stop(self) -> None:
        await self._client.disconnect()
        logger.info("WebSocket disconnected")
