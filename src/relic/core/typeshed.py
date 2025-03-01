"""
Provides a version safe interface for retrieving attributes from the typing / typing_extensions modules.
"""

# mypy: ignore-errors
# pylint: skip-file


try:  # 3.10+
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

try:  # 3.12+
    from collections.abc import Buffer
except ImportError:
    from typing_extensions import Buffer

try:  # 3.12- (Use backport if found, otherwise assume stdlib meets minimum requirements)
    from importlib_metadata import entry_points
except ImportError:
    from importlib.metadata import entry_points

__all__ = ["TypeAlias", "Buffer", "entry_points"]
