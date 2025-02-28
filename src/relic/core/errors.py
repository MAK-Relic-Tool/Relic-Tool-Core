"""
Errors shared across all Relic Tools.
"""

from __future__ import annotations

from typing import Any, Optional, TypeVar, Generic


def _print_mismatch(name: str, received: Optional[Any], expected: Optional[Any]) -> str:
    """
    Constructs a string detailing a mismatch between a received and expected input

    :param name: The name of the variable which received unexpected input
    :type name: str

    :param received: The value of the received input
    :type received: Optional[Any]

    :param expected: The value(s) of the expected input
    :type expected: Optional[Any]

    :return: A string formatted as one of the following (varies by input)
        'Unexpcted {name}!'
        'Unexpcted {name}; got {recieved}!'
        'Unexpcted {name}; expected {expected}!'
        'Unexpcted {name}; got {recieved}, expected {expected}!'

    :rtype: str
    """

    msg = f"Unexpected {name}"
    if received is not None or expected is not None:
        msg += ";"
    if received is not None:
        msg += f" got `{str(received)}`"
    if received is not None and expected is not None:
        msg += ","
    if expected is not None:
        msg += f" expected `{str(expected)}`"
    return msg + "!"


_T = TypeVar("_T")


class RelicToolError(Exception):
    """
    An error was raised by the relic tool.

    All custom errors in this library and it's plugins should inherit from this class.
    """


class CliError(RelicToolError):
    """
    An error was raised by the command line interface.

    All command-line errors in this library and it's plugins should inherit from this class.
    """


class UnboundCommandError(CliError):
    """
    A command was defined in the CLI, but its function was not bound.

    :param name: The name of the command that was not bound.
    :type name: str
    """

    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return f"The '{self._name}' command was defined, but not bound to a function."


class MismatchError(Generic[_T], RelicToolError):
    """
    An error where a received value did not match the expected value.
    """

    def __init__(
        self, name: str, received: Optional[_T] = None, expected: Optional[_T] = None
    ):
        super().__init__()
        self.name = name
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return _print_mismatch(self.name, self.received, self.expected)


class MagicMismatchError(MismatchError[bytes]):
    """
    An error where a file's magic word did not match the expected value.

    This typically means the file is empty, corrupted, or is not the specified file format.
    """


class RelicSerializationError(RelicToolError):
    """
    An error was raised while serializing an object.
    """


class RelicSerializationSizeError(RelicSerializationError):
    """
    While serializing an object, the size of the binary buffer did not match the expected read or write size
    """

    def __init__(
        self,
        msg: str = "Size Mismatch",
        size: Optional[int] = None,
        expected: Optional[int] = None,
        payload: Optional[str] = None,
    ):
        self.size = (size,)
        self.expected = expected
        self.payload = payload
        super().__init__(msg)


__all__ = [
    "RelicToolError",
    "MismatchError",
    "MagicMismatchError",
    "CliError",
    "UnboundCommandError",
    "RelicSerializationError",
    "RelicSerializationSizeError",
]
