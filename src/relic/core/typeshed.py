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

__all__ = ["TypeAlias", "Buffer"]
