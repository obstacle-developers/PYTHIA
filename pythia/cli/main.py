"""Command-line entry point for the PYTHIA package foundation."""

from __future__ import annotations

from pythia import PACKAGE_NAME, PACKAGE_STATUS
from pythia.core.safety import FORBIDDEN_DISCOVERY_PHRASES, safe_status_labels

AVAILABLE_MODULES = ("core", "reasoning", "omega", "cli")


def main() -> None:
    """Print package foundation status."""
    print(f"package name: {PACKAGE_NAME}")
    print(f"package status: {PACKAGE_STATUS}")
    print(f"available modules: {', '.join(AVAILABLE_MODULES)}")
    print(f"safety rules loaded: {len(FORBIDDEN_DISCOVERY_PHRASES)} forbidden phrases")
    print(f"status labels: {', '.join(safe_status_labels())}")


if __name__ == "__main__":
    main()
