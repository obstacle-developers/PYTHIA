from pathlib import Path


def test_expected_package_layout_exists():
    expected = [
        "pythia/__init__.py",
        "pythia/core/__init__.py",
        "pythia/core/config.py",
        "pythia/core/db.py",
        "pythia/core/export.py",
        "pythia/core/jsonl.py",
        "pythia/core/safety.py",
        "pythia/reasoning/__init__.py",
        "pythia/reasoning/retrieval.py",
        "pythia/reasoning/constraints.py",
        "pythia/reasoning/ranking.py",
        "pythia/reasoning/recommendations.py",
        "pythia/reasoning/traces.py",
        "pythia/reasoning/evaluator.py",
        "pythia/reasoning/reports.py",
        "pythia/omega/__init__.py",
        "pythia/omega/clustering.py",
        "pythia/omega/fingerprints.py",
        "pythia/omega/candidates.py",
        "pythia/omega/falsification.py",
        "pythia/cli/__init__.py",
        "pythia/cli/main.py",
    ]
    for path in expected:
        assert Path(path).is_file(), path
