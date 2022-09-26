"""
Errors shared across all Relic Tools.
"""
from typing import Any, Optional, TypeVar, Generic


def _print_mismatch(name: str, received: Optional[Any], expected: Optional[Any]) -> str:
    msg = f"Unexpected {name}"
    if received or expected:
        msg += ";"
    if received:
        msg += f" got `{str(received)}`"
    if received and expected:
        msg += ","
    if expected:
        msg += f" expected `{str(expected)}`"
    return msg + "!"


T = TypeVar("T")


class RelicToolError(Exception):
    """
    Marks an Error as a RelicToolError. Does nothing special.
    """


class MismatchError(Generic[T], RelicToolError):
    """
    An error where an expected value did not match the actual received value.
    """

    def __init__(
        self, name: str, received: Optional[T] = None, expected: Optional[T] = None
    ):
        super().__init__()
        self.name = name
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return _print_mismatch(self.name, self.received, self.expected)


__all__ = ["T", "MismatchError", "RelicToolError"]
