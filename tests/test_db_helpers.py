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


def test_db_helpers_validate_table_identifiers():
    connection = connect(":memory:")
    try:
        connection.execute("CREATE TABLE valid_name_1 (id INTEGER PRIMARY KEY)")
        assert table_exists(connection, "valid_name_1")
        assert row_count(connection, "valid_name_1") == 0

        for table_name in ("examples; DROP TABLE examples", 'examples"quote', "examples name"):
            with pytest.raises(ValueError, match="unsafe SQLite identifier"):
                table_exists(connection, table_name)
            with pytest.raises(ValueError, match="unsafe SQLite identifier"):
                row_count(connection, table_name)
    finally:
        connection.close()
