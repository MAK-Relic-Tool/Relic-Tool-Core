import os
from typing import BinaryIO, Optional, Type

from relic.core.errors import MismatchError


class MagicWord:
    def __init__(
        self,
        expected: bytes,
        name: str,
        *,
        err_cls: Type[MismatchError[bytes]] = MismatchError
    ):
        self._expected = expected
        self._name = name
        self._default_err_cls = err_cls

    def __len__(self):
        return len(self._expected)

    def __eq__(self, other):
        if isinstance(other, MagicWord):
            return self._expected == other._expected
        else:
            return self._expected == other

    def read(self, stream: BinaryIO, advance: bool = False) -> bytes:
        def _read():
            return stream.read(len(self))

        if advance:
            return _read()

        now = stream.tell()
        buffer = _read()
        stream.seek(now, os.SEEK_SET)
        return buffer

    def check(self, stream: BinaryIO, advance: bool = False) -> bool:
        read = self.read(stream, advance)
        return read == self._expected

    def validate(
        self,
        stream: BinaryIO,
        advance: bool = False,
        *,
        name: Optional[str] = None,
        err_cls: Optional[Type[MismatchError[bytes]]] = None
    ):
        read = self.read(stream, advance)
        if read != self._expected:
            if name is None:
                name = self._name
            if err_cls is None:
                err_cls = self._default_err_cls

            raise err_cls(name, read, self._expected)
