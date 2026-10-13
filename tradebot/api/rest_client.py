"""REST client for the Bitpin API (market data + authentication)."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import httpx

from tradebot.config import Config

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MarketInfo:
    symbol: str
    base: str
    quote: str
    tradable: bool
    price_precision: int
    base_amount_precision: int
    quote_amount_precision: int
    suspended: bool = False


@dataclass(frozen=True)
class CommissionInfo:
    maker: float
    taker: float

    @staticmethod
    def _to_fraction(value: float) -> float:
        """Normalize a Bitpin commission value to a fraction.

        The live API returns fees as fractions (e.g. 0.003 == 0.3%) while
        documentation samples show percent-style numbers (0.3 == 0.3%).
        Values >= 0.05 are interpreted as percent; smaller ones as fractions.
        """
        return value / 100.0 if value >= 0.05 else value

    @property
    def maker_fraction(self) -> float:
        return self._to_fraction(self.maker)

    @property
    def taker_fraction(self) -> float:
        return self._to_fraction(self.taker)


class BitpinRestClient:
    """Thin async wrapper over the public and authenticated REST endpoints."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._http = httpx.AsyncClient(
            base_url=config.api.base_url,
            timeout=config.api.timeout_sec,
        )
        self._access_token: str | None = None
        self._token_obtained_at: float = 0.0
        self._market_info: MarketInfo | None = None
        self._commission: CommissionInfo | None = None

    async def close(self) -> None:
        await self._http.aclose()

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    async def authenticate(self) -> None:
        """Exchange API key/secret for an access token."""
        response = await self._http.post(
            "/api/v1/usr/authenticate/",
            json={
                "api_key": self._config.api.api_key,
                "secret_key": self._config.api.secret_key,
            },
        )
        response.raise_for_status()
        payload = response.json()
        self._access_token = payload["access"]
        self._token_obtained_at = time.monotonic()
        logger.info("Authenticated; access token acquired")

    async def refresh_access_token(self) -> None:
        """Placeholder for refresh flow; re-authenticates for now.

        Bitpin documents a refresh endpoint, but key/secret re-auth is
        simpler and stays within the 200/day limit when called sparingly.
        """
        await self.authenticate()

    @property
    def access_token(self) -> str | None:
        return self._access_token

    def _auth_headers(self) -> dict[str, str]:
        if not self._access_token:
            raise RuntimeError("Not authenticated; call authenticate() first")
        return {"Authorization": f"Bearer {self._access_token}"}

    # ------------------------------------------------------------------
    # Market metadata
    # ------------------------------------------------------------------

    async def get_market_info(self, symbol: str) -> MarketInfo:
        """Fetch precision and tradability metadata for a market."""
        response = await self._http.get("/api/v1/mkt/markets/")
        response.raise_for_status()
        for item in response.json():
            if item.get("symbol") == symbol:
                info = MarketInfo(
                    symbol=item["symbol"],
                    base=item["base"],
                    quote=item["quote"],
                    tradable=bool(item.get("tradable", False)),
                    price_precision=int(item.get("price_precision", 0)),
                    base_amount_precision=int(
                        item.get("base_amount_precision", 8)
                    ),
                    quote_amount_precision=int(
                        item.get("quote_amount_precision", 0)
                    ),
                    suspended=bool(item.get("suspended", False)),
                )
                self._market_info = info
                return info
        raise LookupError(f"Market not found: {symbol}")

    @property
    def market_info(self) -> MarketInfo | None:
        return self._market_info

    # ------------------------------------------------------------------
    # Commissions
    # ------------------------------------------------------------------

    async def get_commission(self, symbol: str) -> CommissionInfo:
        """Fetch maker/taker fees for a market (authenticated)."""
        response = await self._http.get(
            "/api/v1/mkt/commissions/",
            headers=self._auth_headers(),
        )
        response.raise_for_status()
        for item in response.json():
            if item.get("symbol") == symbol:
                info = CommissionInfo(
                    maker=float(item["maker"]),
                    taker=float(item["taker"]),
                )
                self._commission = info
                return info
        raise LookupError(f"Commission not found for market: {symbol}")

    @property
    def commission(self) -> CommissionInfo | None:
        return self._commission

    # ------------------------------------------------------------------
    # Market data
    # ------------------------------------------------------------------

    async def get_orderbook_snapshot(self, symbol: str) -> dict:
        """Fetch a fresh order-book snapshot (top 20 levels per side)."""
        response = await self._http.get(f"/api/v1/mth/orderbook/{symbol}/")
        response.raise_for_status()
        return response.json()

    async def get_ticker(self, symbol: str) -> dict:
        """Fetch the ticker list and extract one symbol."""
        response = await self._http.get("/api/v1/mkt/tickers/")
        response.raise_for_status()
        for item in response.json():
            if item.get("symbol") == symbol:
                return item
        raise LookupError(f"Ticker not found: {symbol}")
