"""Safe export helpers for JSON, Markdown, and ZIP files."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any, Iterable

_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")


def ensure_export_dir(path: str | Path) -> Path:
    """Create and return an export directory path."""
    export_dir = Path(path)
    export_dir.mkdir(parents=True, exist_ok=True)
    if not export_dir.is_dir():
        raise NotADirectoryError(export_dir)
    return export_dir


def _resolve_output(directory: str | Path, filename: str, suffix: str) -> Path:
    if Path(filename).name != filename:
        raise ValueError("filename must not include path components")
    if not filename.endswith(suffix):
        raise ValueError(f"filename must end with {suffix}")
    return ensure_export_dir(directory) / filename


def _safe_archive_name(name: str | Path) -> str:
    """Return a POSIX ZIP member name after rejecting traversal forms."""
    raw_name = str(name)
    if not raw_name:
        raise ValueError("archive member name must not be empty")
    if "\\" in raw_name:
        raise ValueError("archive member name must use POSIX separators")
    if _WINDOWS_DRIVE_RE.match(raw_name):
        raise ValueError("archive member name must not include a Windows drive prefix")

    path = Path(raw_name)
    if path.is_absolute() or raw_name.startswith("/"):
        raise ValueError("archive member name must not be absolute")

    parts = raw_name.split("/")
    if any(part in {"", ".."} for part in parts):
        raise ValueError("archive member name must not traverse directories")
    return "/".join(parts)


def write_json(directory: str | Path, filename: str, data: Any) -> Path:
    """Write JSON data into an export directory and return the file path."""
    output = _resolve_output(directory, filename, ".json")
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def write_markdown(directory: str | Path, filename: str, content: str) -> Path:
    """Write Markdown content into an export directory and return the file path."""
    output = _resolve_output(directory, filename, ".md")
    output.write_text(content, encoding="utf-8")
    return output


def write_zip(directory: str | Path, filename: str, files: Iterable[str | Path]) -> Path:
    """Create a ZIP archive containing the provided files by basename."""
    output = _resolve_output(directory, filename, ".zip")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in files:
            path = Path(file_path)
            if not path.is_file():
                raise FileNotFoundError(path)
            archive.write(path, arcname=_safe_archive_name(path.name))
    return output
