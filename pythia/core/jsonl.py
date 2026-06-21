"""Append-only JSON Lines helpers for PYTHIA records."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

JsonRecord = Mapping[str, Any]


def validate_record_has_keys(record: JsonRecord, required_keys: Iterable[str]) -> None:
    """Raise ValueError if a JSONL record is missing required keys."""
    missing = [key for key in required_keys if key not in record]
    if missing:
        raise ValueError(f"record missing required keys: {', '.join(sorted(missing))}")


def append_jsonl(path: str | Path, record: JsonRecord) -> Path:
    """Append one JSON object to a JSON Lines file and return the file path.

    The file is opened in append mode, so existing records are not read into
    memory. Parent directories are created when needed.
    """
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, separators=(",", ":"))
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{line}\n")
    return output_path


def append_jsonl_many(path: str | Path, records: Iterable[JsonRecord]) -> Path:
    """Append JSON objects to a JSON Lines file while opening it once.

    Records are streamed from the iterable and are not accumulated in memory.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        for record in records:
            if not isinstance(record, Mapping):
                raise TypeError("record must be a mapping")
            line = json.dumps(record, sort_keys=True, separators=(",", ":"))
            handle.write(f"{line}\n")
    return output_path


def iter_jsonl(path: str | Path):
    """Yield JSON objects from a JSON Lines file, streaming line by line."""
    input_path = Path(path)
    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number} of {input_path}") from exc
