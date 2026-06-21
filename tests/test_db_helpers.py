import pytest

from pythia.core.db import connect, list_tables, row_count, table_exists


def test_db_helpers_with_in_memory_sqlite():
    connection = connect(":memory:")
    try:
        connection.execute("CREATE TABLE examples (id INTEGER PRIMARY KEY, label TEXT)")
        connection.executemany("INSERT INTO examples (label) VALUES (?)", [("a",), ("b",)])
        assert table_exists(connection, "examples")
        assert not table_exists(connection, "missing")
        assert list_tables(connection) == ["examples"]
        assert row_count(connection, "examples") == 2
        with pytest.raises(ValueError):
            row_count(connection, "missing")
    finally:
        connection.close()
