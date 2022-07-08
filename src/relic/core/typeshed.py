"""
Provides a version safe interface for retrieving attributes from the typing / typing_extensions modules.
"""
import sys

__version_pair = sys.version_info[0:2]
if __version_pair >= (3, 10):
    from typing import TypeAlias  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypeAlias  # pylint: disable=no-name-in-module

__all__ = [TypeAlias]
