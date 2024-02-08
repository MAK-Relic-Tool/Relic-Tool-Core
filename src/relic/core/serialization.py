"""
Module containing tools for serialization.
"""

from typing import BinaryIO, Optional, Type, Any

from relic.core.errors import MismatchError, MagicMismatchError
from relic.core.lazyio import BinaryWindow


class MagicWord:
    """
    Create a Magic Word; which can read, check or validate (check withe error) from a binary stream.

    :param expected: The magic word to match
    :type expected: bytes

    :param name: The default name for the magic word; this will be used when a Mismatch Error is raised
    :type name: str

    :param err_cls: The error class to raise when validate fails, By default, MagicMismatchError
    :type err_cls: Type[MismatchError[bytes]], optional
    """

    def __init__(
        self,
        expected: bytes,
        name: str,
        *,
        err_cls: Type[MismatchError[bytes]] = MagicMismatchError,
    ):
        self._expected = expected
        self._name = name
        self._default_err_cls = err_cls

    def __len__(self) -> int:
        return len(self._expected)

    def __eq__(self, other: Any) -> bool:
        result: bool
        if isinstance(other, MagicWord):
            result = self._expected == other._expected
        else:
            result = self._expected == other
        return result

    def read(self, stream: BinaryIO, advance: bool = False) -> bytes:
        """
        Reads a buffer from the stream that is the size of the magic word.

        :param stream: The stream to read from
        :type stream: BinaryIO

        :param advance: If true, the IO pointer will be updated
            By default, this is False
        :type advance: bool, optional

        :returns: A bytes buffer that is the size of the magic word
        :rtype: bytes
        """
        size = len(self)
        if not advance:
            with BinaryWindow(
                stream, start=stream.tell(), size=size
            ) as window:  # Use window to cheese 'peek' behaviour
                buffer = window.read()
        else:
            buffer = stream.read(size)

        return buffer

    def write(self, stream: BinaryIO) -> int:
        """
        Writes the magic word to the stream.

        :param stream: The stream to write to
        :type stream: BinaryIO

        :rtype: int
        :returns: The number of bytes written.
        """
        return stream.write(self._expected)

    def check(self, stream: BinaryIO, advance: bool = False) -> bool:
        """
        Checks that the magic word is the next value in the stream and returns the result.

        :param stream: The stream to check for the magic word
        :type stream: BinaryIO

        :param advance: If true, the IO pointer will be updated.
            By default, this is False

        :type advance: bool

        :returns: True if the magic word is correct, False otherwise
        :rtype: bool
        """
        read = self.read(stream, advance)
        return read == self._expected

    def validate(
        self,
        stream: BinaryIO,
        advance: bool = False,
        *,
        name: Optional[str] = None,
        err_cls: Optional[Type[MismatchError[bytes]]] = None,
    ) -> None:
        """
        Validates that the magic word is the next value in the stream, raises an error if it is not.

        :param stream: The stream to check for the magic word
        :type stream: BinaryIO

        :param advance: If true, the IO pointer will be updated
            By default, this is False
        :type advance: bool

        :param name: A custom name to use when raising a Mismatch Error
        :type name: str, optional

        :param err_cls: A custom error class to raise instead of the default specified on creation
        :type err_cls: Type[MismatchError[bytes]]

        :raises MismatchError[bytes]: The value read was not the expected magic word
        """

        read = self.read(stream, advance)
        if read != self._expected:
            if name is None:
                name = self._name
            if err_cls is None:
                err_cls = self._default_err_cls

            raise err_cls(name, read, self._expected)
