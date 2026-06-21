from pathlib import Path

import pytest

from pythia.core.safety import (
    assert_no_forbidden_discovery_language,
    assert_record_uses_safe_language,
    find_forbidden_discovery_language,
    find_forbidden_language_in_value,
    find_probability_misuse,
    safe_status_labels,
    scan_source_for_dynamic_execution,
)


def test_forbidden_discovery_language_checker():
    text = "PYTHIA discovered a particle discovered pattern, but that claim is not allowed."
    assert "pythia discovered" in find_forbidden_discovery_language(text)
    assert "particle discovered" in find_forbidden_discovery_language(text)
    assert find_forbidden_discovery_language("candidate signal pattern requiring review") == []


def test_probability_misuse_phrase_checker():
    assert "100% probability" in find_probability_misuse("This has 100% probability.")
    assert find_probability_misuse("candidate explanation with uncertainty") == []


def test_safe_status_labels():
    labels = safe_status_labels()
    assert "PASS" in labels
    assert "VERIFIED PASS" in labels


def test_source_scanner_detects_eval_and_exec(tmp_path: Path):
    source = tmp_path / "unsafe.py"
    source.write_text("eval('1 + 1')\nexec('x = 1')\n", encoding="utf-8")
    findings = scan_source_for_dynamic_execution(tmp_path)
    assert source in findings
    assert findings[source] == ["eval(", "exec("]


def test_centralized_safety_catches_unsafe_strings():
    assert "new physics found" in find_forbidden_language_in_value("new physics found")
    with pytest.raises(ValueError, match="unsafe discovery language"):
        assert_no_forbidden_discovery_language("confirmed signal")


def test_centralized_safety_catches_nested_dictionaries():
    record = {"outer": [{"inner": ("safe", "discovery confirmed")}]}
    with pytest.raises(ValueError, match="unsafe discovery language"):
        assert_record_uses_safe_language(record)
