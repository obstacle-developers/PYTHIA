import json
import zipfile

import pytest

from pythia.core.export import ensure_export_dir, write_json, write_markdown, write_zip


def test_export_helpers_write_json_markdown_and_zip(tmp_path):
    export_dir = ensure_export_dir(tmp_path / "exports")
    json_path = write_json(export_dir, "result.json", {"status": "PASS"})
    md_path = write_markdown(export_dir, "report.md", "# Audit result\n")
    zip_path = write_zip(export_dir, "bundle.zip", [json_path, md_path])

    assert json.loads(json_path.read_text(encoding="utf-8")) == {"status": "PASS"}
    assert md_path.read_text(encoding="utf-8") == "# Audit result\n"
    with zipfile.ZipFile(zip_path) as archive:
        assert sorted(archive.namelist()) == ["report.md", "result.json"]


def test_safe_archive_name_rejects_traversal_and_absolute_names():
    from pythia.core.export import _safe_archive_name

    assert _safe_archive_name("safe/nested.txt") == "safe/nested.txt"
    for name in ("../evil.txt", "/tmp/evil.txt", r"C:\evil.txt", "safe/../evil.txt", ""):
        with pytest.raises(ValueError):
            _safe_archive_name(name)


def test_write_zip_normal_output_still_works(tmp_path):
    export_dir = ensure_export_dir(tmp_path / "exports")
    data_path = tmp_path / "safe.txt"
    data_path.write_text("safe\n", encoding="utf-8")

    zip_path = write_zip(export_dir, "safe_bundle.zip", [data_path])

    with zipfile.ZipFile(zip_path) as archive:
        assert archive.namelist() == ["safe.txt"]
        assert archive.read("safe.txt").decode("utf-8") == "safe\n"
