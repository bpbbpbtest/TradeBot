"""Live dashboard state: book, features, decisions, trades for the UI."""

from __future__ import annotations

import time
from collections import deque
from typing import Any

from tradebot.data.orderbook import OrderBook

_BOOK_LEVELS_SHOWN = 12


class DashboardState:
    """Single-threaded (asyncio loop) store feeding the browser dashboard."""

    def __init__(self, max_history: int = 2000) -> None:
        self._history: deque[dict[str, Any]] = deque(maxlen=max_history)
        self._actions: deque[dict[str, Any]] = deque(maxlen=300)
        self._matches: deque[dict[str, Any]] = deque(maxlen=300)
        self._trades: deque[dict[str, Any]] = deque(maxlen=100)
        self._params: dict[str, Any] = {}
        self._last_book: dict[str, Any] = {}
        self._features: dict[str, Any] = {}
        self._position: dict[str, Any] = {}
        self._halt: dict[str, Any] = {"active": False, "reason": ""}
        self._last_action = ""
        self._last_point_ts = 0.0
        self._known_trades = 0
        self._seq = 0
        self._started_at = time.time()
        self._account: dict[str, Any] = {}
        self._status: dict[str, Any] = {
            "running": False,
            "symbol": "",
            "error": "",
        }

    # ------------------------------------------------------------------
    # Run lifecycle (start/stop/symbol switch from the dashboard)
    # ------------------------------------------------------------------

    def set_status(self, running: bool, symbol: str, error: str = "") -> None:
        self._status = {
            "running": running,
            "symbol": symbol,
            "error": error or "",
        }

    def reset_run_data(self) -> None:
        """Clear per-run buffers so a new symbol/run starts clean."""
        self._history.clear()
        self._actions.clear()
        self._matches.clear()
        self._trades.clear()
        self._features = {}
        self._position = {}
        self._account = {}
        self._last_book = {}
        self._halt = {"active": False, "reason": ""}
        self._last_action = ""
        self._last_point_ts = 0.0
        self._known_trades = 0

    # ------------------------------------------------------------------
    # Feed methods (called from the bot's asyncio loop)
    # ------------------------------------------------------------------

    def set_params(self, params: dict[str, Any]) -> None:
        self._params = params

    def on_book(self, book: OrderBook, now: float) -> None:
        self._last_book = self._book_payload(book, now)
        self._maybe_append_point(book, now)

    def on_matches(self, payload: dict[str, Any]) -> None:
        matches = payload.get("matches")
        if not isinstance(matches, list):
            return
        for item in matches:
            if not isinstance(item, dict):
                continue
            try:
                self._matches.append(
                    {
                        "ts": time.time(),
                        "price": float(item["price"]),
                        "amount": float(item["base_amount"]),
                        "side": str(item.get("side", "")),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue

    def on_eval(
        self,
        *,
        feats: Any,
        score: float,
        persistent: bool,
        dominant: int,
        action: str,
        engine: Any,
        book: OrderBook,
        halted: bool,
        halt_reason: str,
        now: float,
    ) -> None:
        self._features = {
            "valid": bool(getattr(feats, "valid", False)),
            "score": round(score, 6),
            "depth_imbalance": round(getattr(feats, "depth_imbalance", 0.0), 6),
            "micro_m": round(getattr(feats, "micro_m", 0.0), 6),
            "ofi_z": round(getattr(feats, "ofi_z", 0.0), 6),
            "ofi_raw": round(getattr(feats, "ofi_raw", 0.0), 6),
            "ofi_samples": getattr(feats, "ofi_samples", 0),
            "mid": round(getattr(feats, "mid", 0.0), 2),
            "spread_pct": round(getattr(feats, "spread_pct", 0.0), 8),
            "bid_volume_l1": round(getattr(feats, "bid_volume_l1", 0.0), 6),
            "ask_volume_l1": round(getattr(feats, "ask_volume_l1", 0.0), 6),
            "persistent": persistent,
            "dominant": dominant,
        }
        self._last_action = action
        self._actions.append(
            {
                "ts": now,
                "score": round(score, 4),
                "action": action,
                "mid": round(getattr(feats, "mid", 0.0) or 0.0, 1),
            }
        )
        self._halt = {"active": halted, "reason": halt_reason or ""}
        self._sync_trades(engine)
        self._position = self._position_payload(engine, book, now)
        self._account = self._account_payload(engine, book)
        self._last_book = self._book_payload(book, now)
        self._maybe_append_point(book, now)

    # ------------------------------------------------------------------
    # Payload builders
    # ------------------------------------------------------------------

    def _sync_trades(self, engine: Any) -> None:
        closed = engine.account.trades
        while self._known_trades < len(closed):
            trade = closed[self._known_trades]
            self._known_trades += 1
            holding = (
                (trade.exit_time - trade.entry_time)
                if trade.exit_time is not None
                else None
            )
            pnl_pct = (
                trade.pnl_irt / trade.quote_spent * 100
                if trade.quote_spent > 0
                else None
            )
            self._trades.append(
                {
                    "id": trade.trade_id,
                    "entry_ts": trade.entry_time,
                    "entry_price": trade.entry_price,
                    "exit_ts": trade.exit_time,
                    "exit_price": trade.exit_price,
                    "qty": trade.quantity,
                    "quote_spent": round(trade.quote_spent, 2),
                    "quote_received": round(trade.quote_received, 2),
                    "fee_entry": round(trade.fee_entry, 2),
                    "fee_exit": round(trade.fee_exit, 2),
                    "fees_total": round(trade.fee_entry + trade.fee_exit, 2),
                    "holding_sec": holding,
                    "pnl": round(trade.pnl_irt, 2),
                    "pnl_pct": round(pnl_pct, 4) if pnl_pct is not None else None,
                    "reason": trade.exit_reason,
                    "score_at_entry": round(trade.score_at_entry, 4),
                }
            )

    def _account_payload(self, engine: Any, book: OrderBook) -> dict[str, Any]:
        trades = engine.account.trades
        realized = sum(t.pnl_irt for t in trades)
        fees = sum(t.fee_entry + t.fee_exit for t in trades)
        open_trade = engine.account.open_trade
        open_unrealized = 0.0
        if open_trade is not None:
            fees += open_trade.fee_entry
            open_unrealized = engine.unrealized_pnl_irt(book)
        wins = sum(1 for t in trades if t.pnl_irt > 0)
        losses = len(trades) - wins
        pnls = [t.pnl_irt for t in trades]
        equity = engine.equity_irt(book)
        initial = float(self._params.get("capital_irt") or equity or 1.0)
        return {
            "initial": initial,
            "cash": round(engine.account.cash_irt, 2),
            "equity": round(equity, 2),
            "realized_pnl": round(realized, 2),
            "unrealized_pnl": round(open_unrealized, 2),
            "fees_paid": round(fees, 2),
            "total_trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / len(trades) * 100, 1) if trades else None,
            "avg_pnl": round(sum(pnls) / len(pnls), 2) if pnls else 0.0,
            "best_pnl": round(max(pnls), 2) if pnls else 0.0,
            "worst_pnl": round(min(pnls), 2) if pnls else 0.0,
            "roi_pct": round((equity - initial) / initial * 100, 3),
        }

    @staticmethod
    def _book_payload(book: OrderBook, now: float) -> dict[str, Any]:
        mid = book.mid
        spread = book.spread
        bid = book.best_bid
        ask = book.best_ask
        return {
            "mid": mid,
            "bid": bid.price if bid else None,
            "ask": ask.price if ask else None,
            "spread": spread,
            "spread_bps": (spread / mid * 10000) if spread and mid else None,
            "age": book.age_sec(now) if book.received_at else None,
            "bids": [
                [lvl.price, lvl.volume] for lvl in book.bids[:_BOOK_LEVELS_SHOWN]
            ],
            "asks": [
                [lvl.price, lvl.volume] for lvl in book.asks[:_BOOK_LEVELS_SHOWN]
            ],
        }

    def _position_payload(self, engine: Any, book: OrderBook, now: float) -> dict[str, Any]:
        account = engine.account
        risk = self._params.get("risk", {})
        payload: dict[str, Any] = {
            "state": account.state.value if hasattr(account.state, "value") else str(account.state),
            "cash": round(account.cash_irt, 2),
            "equity": round(engine.equity_irt(book), 2),
            "base_holding": account.base_holding,
            "entry": None,
            "entry_ts": None,
            "qty": 0.0,
            "u_pnl": 0.0,
            "stop": None,
            "take": None,
            "holding_sec": 0.0,
            "score_at_entry": None,
        }
        trade = account.open_trade
        if trade is not None:
            entry = trade.entry_price
            stop_pct = float(risk.get("stop_loss_pct", 0.0))
            take_pct = float(risk.get("take_profit_pct", 0.0))
            fee_taker = float(self._params.get("fees", {}).get("taker", 0.0))
            bid = book.best_bid.price if book.best_bid else None
            u_pnl = engine.unrealized_pnl_irt(book)
            u_pnl_pct = (
                u_pnl / trade.quote_spent * 100 if trade.quote_spent > 0 else None
            )
            stop = entry * (1 - stop_pct) if entry else None
            take = entry * (1 + take_pct) if entry else None
            dist_stop_bps = (
                (bid - stop) / bid * 10000 if bid and stop else None
            )
            dist_take_bps = (
                (take - bid) / bid * 10000 if bid and take else None
            )
            net_if_exit = None
            if bid and account.base_holding > 0:
                gross = account.base_holding * bid
                net_if_exit = round(
                    gross * (1 - fee_taker) - trade.quote_spent - trade.fee_entry,
                    2,
                )
            payload.update(
                {
                    "entry": entry,
                    "entry_ts": trade.entry_time,
                    "qty": account.base_holding,
                    "quote_spent": round(trade.quote_spent, 2),
                    "fee_entry": round(trade.fee_entry, 2),
                    "u_pnl": round(u_pnl, 2),
                    "u_pnl_pct": round(u_pnl_pct, 4) if u_pnl_pct is not None else None,
                    "stop": stop,
                    "take": take,
                    "dist_stop_bps": round(dist_stop_bps, 1) if dist_stop_bps is not None else None,
                    "dist_take_bps": round(dist_take_bps, 1) if dist_take_bps is not None else None,
                    "net_if_exit": net_if_exit,
                    "holding_sec": max(0.0, now - trade.entry_time),
                    "score_at_entry": trade.score_at_entry,
                }
            )
        return payload

    def _maybe_append_point(self, book: OrderBook, now: float) -> None:
        if now - self._last_point_ts < 1.0:
            return
        mid = book.mid
        bid = book.best_bid
        ask = book.best_ask
        if mid is None or bid is None or ask is None:
            return
        self._history.append(
            {
                "ts": now,
                "mid": mid,
                "bid": bid.price,
                "ask": ask.price,
                "score": self._features.get("score", 0.0),
                "depth": self._features.get("depth_imbalance", 0.0),
                "micro": self._features.get("micro_m", 0.0),
                "ofi_z": self._features.get("ofi_z", 0.0),
            }
        )
        self._last_point_ts = now

    def _markers(self) -> list[dict[str, Any]]:
        markers: list[dict[str, Any]] = []
        for trade in list(self._trades)[-20:]:
            markers.append(
                {"ts": trade["entry_ts"], "price": trade["entry_price"], "type": "entry"}
            )
            if trade["exit_ts"]:
                markers.append(
                    {"ts": trade["exit_ts"], "price": trade["exit_price"], "type": "exit"}
                )
        if self._position.get("entry") and self._position.get("entry_ts"):
            markers.append(
                {
                    "ts": self._position["entry_ts"],
                    "price": self._position["entry"],
                    "type": "entry",
                }
            )
        return markers

    def history(self) -> list[dict[str, Any]]:
        return list(self._history)

    def _open_trade_row(self) -> dict[str, Any] | None:
        pos = self._position
        if pos.get("state") != "long" or not pos.get("entry"):
            return None
        return {
            "id": "open",
            "live": True,
            "entry_ts": pos.get("entry_ts"),
            "entry_price": pos.get("entry"),
            "exit_ts": None,
            "exit_price": None,
            "qty": pos.get("qty"),
            "fees_total": pos.get("fee_entry"),
            "pnl": pos.get("u_pnl"),
            "pnl_pct": pos.get("u_pnl_pct"),
            "holding_sec": pos.get("holding_sec"),
            "reason": "OPEN",
            "net_if_exit": pos.get("net_if_exit"),
            "dist_stop_bps": pos.get("dist_stop_bps"),
            "dist_take_bps": pos.get("dist_take_bps"),
        }

    def tick(self) -> dict[str, Any]:
        self._seq += 1
        open_row = self._open_trade_row()
        trades = (
            ([open_row] if open_row else []) + list(self._trades)[-30:][::-1]
        )
        return {
            "seq": self._seq,
            "ts": time.time(),
            "uptime_sec": time.time() - self._started_at,
            "params": self._params,
            "status": self._status,
            "book": self._last_book,
            "features": self._features,
            "position": self._position,
            "account": self._account,
            "halt": self._halt,
            "action": self._last_action,
            "recent_actions": list(self._actions)[-60:][::-1],
            "matches": list(self._matches)[-40:][::-1],
            "trades": trades,
            "markers": self._markers(),
            "point": self._history[-1] if self._history else None,
        }
