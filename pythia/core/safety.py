"""Safety checks for PYTHIA package text and source files."""

from __future__ import annotations

from pathlib import Path

FORBIDDEN_DISCOVERY_PHRASES = (
    "pythia discovered",
    "new physics found",
    "confirmed discovery",
    "proved",
    "guaranteed",
    "certain",
    "particle discovered",
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
