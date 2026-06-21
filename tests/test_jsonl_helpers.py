import pytest

from pythia.core.jsonl import append_jsonl, iter_jsonl, validate_record_has_keys


def test_append_jsonl_one_record(tmp_path):
    path = append_jsonl(tmp_path / "nested" / "negative_knowledge.jsonl", {"b": 2, "a": 1})

    assert path.read_text(encoding="utf-8") == '{"a":1,"b":2}\n'


def test_append_jsonl_multiple_records(tmp_path):
    path = tmp_path / "negative_knowledge.jsonl"

    append_jsonl(path, {"id": "first"})
    append_jsonl(path, {"id": "second"})

    assert path.read_text(encoding="utf-8") == '{"id":"first"}\n{"id":"second"}\n'


def test_iter_jsonl_streams_records_and_skips_blank_lines(tmp_path):
    path = tmp_path / "records.jsonl"
    path.write_text('{"id":"one"}\n\n{"id":"two"}\n', encoding="utf-8")

    assert list(iter_jsonl(path)) == [{"id": "one"}, {"id": "two"}]


def test_iter_jsonl_invalid_json_failure(tmp_path):
    path = tmp_path / "records.jsonl"
    path.write_text('{"id":"ok"}\nnot-json\n', encoding="utf-8")

    iterator = iter_jsonl(path)
    assert next(iterator) == {"id": "ok"}
    with pytest.raises(ValueError, match="invalid JSON on line 2"):
        next(iterator)


def test_validate_record_has_keys():
    validate_record_has_keys({"id": "candidate", "status": "review"}, ["id", "status"])

    with pytest.raises(ValueError, match="missing required keys: status"):
        validate_record_has_keys({"id": "candidate"}, ["id", "status"])
