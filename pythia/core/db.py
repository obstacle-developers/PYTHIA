"""Small SQLite helper utilities for PYTHIA.

These helpers intentionally avoid creating project database files by default;
callers may use an in-memory database or an explicit path.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union

DatabaseTarget = Union[str, Path]


def connect(database: DatabaseTarget = ":memory:") -> sqlite3.Connection:
    """Open a SQLite connection for an explicit database target."""
    return sqlite3.connect(str(database))


def list_tables(connection: sqlite3.Connection) -> list[str]:
    """Return user table names in the SQLite database."""
    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    )
    return [row[0] for row in cursor.fetchall()]


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    """Return whether a table exists in the SQLite database."""
    cursor = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? LIMIT 1",
        (table_name,),
    )
    return cursor.fetchone() is not None


def row_count(connection: sqlite3.Connection, table_name: str) -> int:
    """Return row count for an existing table.

    Raises ValueError when the table is not present. Table names are accepted
    only if they exist first, avoiding direct interpolation of untrusted names.
    """
    if not table_exists(connection, table_name):
        raise ValueError(f"table does not exist: {table_name}")
    quoted_name = table_name.replace('"', '""')
    cursor = connection.execute(f'SELECT COUNT(*) FROM "{quoted_name}"')
    return int(cursor.fetchone()[0])
