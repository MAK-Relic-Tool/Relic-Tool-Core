import sys

__version_pair = sys.version_info[0:2]
if __version_pair >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


__all__ = [TypeAlias]
