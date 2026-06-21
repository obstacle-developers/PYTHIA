import json
import zipfile

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
