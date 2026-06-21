"""Safety checks for PYTHIA package text and source files."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
import re

FORBIDDEN_DISCOVERY_PHRASES = (
    "pythia discovered",
    "new physics found",
    "confirmed discovery",
    "proved",
    "guaranteed",
    "certain",
    "particle discovered",
    "new particle discovered",
    "discovery confirmed",
    "new physics found",
    "confirmed signal",
    "new particle",
    "discovered",
)

PROBABILITY_MISUSE_PHRASES = (
    "100% probability",
    "zero uncertainty",
    "statistically certain",
    "guaranteed probability",
)

ALLOWED_WORDING = (
    "candidate signal pattern",
    "candidate explanation",
    "surviving interpretation",
    "human-reviewable",
    "audit result",
    "reasoning trace quality",
)

SAFE_STATUS_LABELS = ("PASS", "VERIFIED PASS", "REVIEW", "WARN", "FAIL", "SKIP")


def find_forbidden_discovery_language(text: str) -> list[str]:
    """Return forbidden discovery phrases found in text, case-insensitively."""
    lowered = text.lower()
    return [phrase for phrase in FORBIDDEN_DISCOVERY_PHRASES if phrase in lowered]


def _phrase_in_text(phrase: str, text: str) -> bool:
    """Return whether a forbidden phrase appears as a token-delimited phrase."""
    return re.search(rf"(?<![a-z0-9_]){re.escape(phrase)}(?![a-z0-9_])", text.lower()) is not None


def find_forbidden_language_in_value(value: Any) -> list[str]:
    """Return forbidden safety-language phrases found in a nested value.

    Dictionaries, lists, tuples, and primitive values are scanned recursively.
    Mapping keys are scanned too because keys can be rendered in audits.
    """
    if isinstance(value, str):
        phrases = FORBIDDEN_DISCOVERY_PHRASES + PROBABILITY_MISUSE_PHRASES
        return [phrase for phrase in phrases if _phrase_in_text(phrase, value)]
    if isinstance(value, Mapping):
        findings: list[str] = []
        for key, nested_value in value.items():
            findings.extend(find_forbidden_language_in_value(key))
            findings.extend(find_forbidden_language_in_value(nested_value))
        return findings
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        findings = []
        for nested_value in value:
            findings.extend(find_forbidden_language_in_value(nested_value))
        return findings
    return []


def assert_no_forbidden_discovery_language(text: str) -> None:
    """Raise ValueError if text contains forbidden discovery/probability language."""
    findings = sorted(set(find_forbidden_language_in_value(text)))
    if findings:
        raise ValueError(f"unsafe discovery language is not allowed: {', '.join(findings)}")


def assert_record_uses_safe_language(record: Mapping[str, Any]) -> None:
    """Raise ValueError if a record contains unsafe language at any nesting level."""
    findings = sorted(set(find_forbidden_language_in_value(record)))
    if findings:
        raise ValueError(f"unsafe discovery language is not allowed: {', '.join(findings)}")


def find_probability_misuse(text: str) -> list[str]:
    """Return probability misuse phrases found in text, case-insensitively."""
    lowered = text.lower()
    return [phrase for phrase in PROBABILITY_MISUSE_PHRASES if phrase in lowered]


def scan_source_for_dynamic_execution(root: str | Path) -> dict[Path, list[str]]:
    """Scan Python source files below root for eval( and exec( usage."""
    root_path = Path(root)
    findings: dict[Path, list[str]] = {}
    for path in root_path.rglob("*.py"):
        if any(part in {".git", "__pycache__", ".venv", "venv"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = [token for token in ("eval(", "exec(") if token in text]
        if hits:
            findings[path] = hits
    return findings


def safe_status_labels() -> tuple[str, ...]:
    """Return accepted status labels for safety-oriented reports."""
    return SAFE_STATUS_LABELS
