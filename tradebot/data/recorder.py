"""Raw data recorder: JSONL for books/matches, CSV for signals."""

from __future__ import annotations

import csv
import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Fixed schema shared by both signal emitters (see main._record_signal*).
# A fixed header means one emitter adding a key can never silently break
# every subsequent DictWriter.writerow call.
_SIGNAL_FIELDS = [
    "ts",
    "score",
    "raw_score",
    "depth_imbalance",
    "micro_m",
    "ofi_z",
    "mid",
    "spread_pct",
    "net_edge",
    "persistent",
    "dominant",
    "action",
]

_write_errors = 0


def _log_write_error(path: Path) -> None:
    """Disk-full / AV-lock errors must never kill the WS callback chain."""
    global _write_errors
    _write_errors += 1
    if _write_errors <= 5 or _write_errors % 1000 == 0:
        logger.warning(
            "Recorder write failed (%d time(s) so far) for %s",
            _write_errors,
            path.name,
        )


class RawDataRecorder:
    """Appends JSONL lines for raw publications and CSV rows for signals."""

    def __init__(self, raw_dir: Path) -> None:
        raw_dir.mkdir(parents=True, exist_ok=True)
        self._raw_dir = raw_dir
        self._book_path = raw_dir / "books.jsonl"
        self._matches_path = raw_dir / "matches.jsonl"
        self._signal_path = raw_dir / "signals.csv"
        self._signals_initialized = False
        # Signals CSV is schema-sensitive; archive any previous run so rows
        # from different schemas/runs never mix in one file.
        if self._signal_path.exists():
            self._signal_path.rename(self._archive_path(raw_dir))

    def archive_signals(self) -> None:
        """Rotate the current signals.csv (e.g. on bot restart/symbol change)."""
        if self._signal_path.exists():
            self._signal_path.rename(self._archive_path(self._raw_dir))
        self._signals_initialized = False

    @staticmethod
    def _archive_path(raw_dir: Path) -> Path:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        candidate = raw_dir / f"signals_{stamp}.csv"
        counter = 1
        while candidate.exists():
            candidate = raw_dir / f"signals_{stamp}_{counter}.csv"
            counter += 1
        return candidate

    def record_book(self, payload: dict[str, Any]) -> None:
        # Recorder stamp goes last so it always wins over a payload "ts".
        self._append_jsonl(self._book_path, {**payload, "ts": time.time()})

    def record_matches(self, payload: dict[str, Any]) -> None:
        self._append_jsonl(self._matches_path, {**payload, "ts": time.time()})

    def record_signal(self, row: dict[str, Any]) -> None:
        write_header = not self._signals_initialized
        try:
            with self._signal_path.open("a", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=_SIGNAL_FIELDS, extrasaction="ignore"
                )
                if write_header:
                    writer.writeheader()
                writer.writerow(row)
                self._signals_initialized = True
        except OSError:
            _log_write_error(self._signal_path)

    @staticmethod
    def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
        try:
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False, default=str))
                handle.write("\n")
        except OSError:
            _log_write_error(path)
