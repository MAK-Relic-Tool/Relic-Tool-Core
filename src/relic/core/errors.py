"""
Errors shared across all Relic Tools.
"""
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


T = TypeVar("T")


class RelicToolError(Exception):
    """
    Marks an Error as a RelicToolError.
    Does nothing special.
    All non-standard errors should inherit from this class.
    """


class CliError(RelicToolError):
    """
    Marks an Error as a Command Line Error.
    Does nothing special.
    All command line errors should inherit from this class.
    """


class UnboundCommandError(CliError):
    """
    A command was defined in the CLI, but its function was not bound.

    If a command is meant to do nothing, a 'do-nothing' function should be bound instead.
    """

    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return f"The '{self._name}' command was defined, but not bound to a function."


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
