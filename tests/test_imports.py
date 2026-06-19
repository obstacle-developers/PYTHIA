import importlib


def test_package_imports_cleanly():
    modules = [
        "pythia",
        "pythia.core.config",
        "pythia.core.db",
        "pythia.core.export",
        "pythia.core.safety",
        "pythia.reasoning.retrieval",
        "pythia.reasoning.constraints",
        "pythia.reasoning.ranking",
        "pythia.reasoning.recommendations",
        "pythia.reasoning.traces",
        "pythia.reasoning.evaluator",
        "pythia.reasoning.reports",
        "pythia.omega.clustering",
        "pythia.omega.fingerprints",
        "pythia.omega.candidates",
        "pythia.omega.falsification",
        "pythia.cli.main",
    ]
    for module in modules:
        importlib.import_module(module)
