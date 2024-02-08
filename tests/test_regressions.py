"""
Tests which ensures releases do not break backwards-compatibility by failing to expose modules/names
"""

import importlib
from typing import List, Iterable, Tuple

import pytest

core__all__ = [
    "errors",
    "typeshed",
]


@pytest.mark.parametrize("submodule", core__all__)
def test_import_module(submodule: str):
    try:
        importlib.import_module(f"relic.core.{submodule}")
    except ImportError:
        raise AssertionError(f"{submodule} is no longer exposed!")


errors__all__ = [
    "MismatchError",
    "RelicToolError",
]
typeshed__all__ = [
    "TypeAlias",
]


def module_imports_helper(submodule: str, all: List[str]) -> Iterable[Tuple[str, str]]:
    return zip([submodule] * len(all), all)


@pytest.mark.parametrize(
    ["submodule", "attribute"],
    [
        *module_imports_helper("errors", errors__all__),
        *module_imports_helper("typeshed", typeshed__all__),
    ],
)
def test_module_imports(submodule: str, attribute: str):
    module = importlib.import_module(f"relic.core.{submodule}")
    _ = getattr(module, attribute)
