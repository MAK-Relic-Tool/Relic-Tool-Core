"""
Provides a version safe interface for retrieving attributes from the typing / typing_extensions modules.
"""
import sys

if sys.version_info[0:2] >= (3, 10):
    from typing import TypeAlias  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypeAlias  # pylint: disable=no-name-in-module

__all__ = [
    "TypeAlias",
]
