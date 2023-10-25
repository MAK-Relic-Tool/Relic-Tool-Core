from __future__ import annotations

import os
import zlib
from contextlib import contextmanager
from types import TracebackType
from typing import (
    BinaryIO,
    Type,
    Iterator,
    AnyStr,
    Iterable,
    Tuple,
    Dict,
    Optional,
    TypeVar,
    Any,
    Literal,
)

from relic.core.errors import RelicToolError

_DEBUG_CLOSE = True


class BinaryWrapper(BinaryIO):
    def __init__(
        self, parent: BinaryIO, close_parent: bool = True, name: Optional[str] = None
    ):
        self._parent = parent
        self._close_parent = close_parent
        self._closed = False
        self._name = name

    def __enter__(self) -> BinaryIO:
        return self

    @property
    def name(self) -> str:
        return self._name or (
            self._parent.name if hasattr(self._parent, "name") else None
        )

    def close(self) -> None:
        if self._close_parent:
            self._parent.close()
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._parent.closed or self._closed

    def fileno(self) -> int:
        return self._parent.fileno()

    def flush(self) -> None:
        return self._parent.flush()

    def isatty(self) -> bool:
        return self._parent.isatty()

    def read(self, __n: int = -1) -> AnyStr:
        return self._parent.read(__n)

    def readable(self) -> bool:
        return self._parent.readable()

    def readline(self, __limit: int = -1) -> AnyStr:
        return self._parent.readline(__limit)

    def readlines(self, __hint: int = -1) -> list[AnyStr]:
        return self._parent.readlines(__hint)

    def seek(self, __offset: int, __whence: int = 0) -> int:
        return self._parent.seek(__offset, __whence)

    def seekable(self) -> bool:
        return self._parent.seekable()

    def tell(self) -> int:
        return self._parent.tell()

    def truncate(self, __size: int | None = ...) -> int:
        return self._parent.truncate()

    def writable(self) -> bool:
        return self._parent.writable()

    def write(self, __s: AnyStr) -> int:
        return self._parent.write(__s)

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        return self._parent.writelines(__lines)

    def __next__(self) -> AnyStr:
        return self._parent.__next__()

    def __iter__(self) -> Iterator[AnyStr]:
        return self._parent.__iter__()

    def __exit__(
        self,
        __t: Type[BaseException] | None,
        __value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        # TODO, this may fail to close the file if an err is thrown
        if self._close_parent:
            return self._parent.__exit__(__t, __value, __traceback)
        return None

    @property
    def mode(self) -> str:
        return self._parent.mode


class BinaryWindow(BinaryWrapper):
    def __init__(
        self,
        parent: BinaryIO,
        start: int,
        size: int,
        close_parent: bool = False,
        name: Optional[str] = None,
    ):
        super().__init__(parent, close_parent, name=name)
        self._now = 0
        self._start = start
        self._size = size

    @property
    def _end(self) -> int:
        return self._start + self._size

    @property
    def _remaining(self) -> int:
        return max(self._size - self._now, 0)

    def tell(self) -> int:
        return self._now

    @contextmanager
    def __rw_ctx(self):
        self.seek(self._now)
        yield
        self._now = super().tell() - self._start

    def seek(self, __offset: int, __whence: int = 0) -> int:
        if __whence == os.SEEK_SET:
            new_now = __offset
        elif __whence == os.SEEK_CUR:
            new_now = __offset + self._now
        elif __whence == os.SEEK_END:
            new_now = self._size - __offset
        else:
            raise ValueError(__whence)

        if new_now < 0:  # or new_now > self._size # Allow seek past end of file?
            __whence_str = {
                os.SEEK_SET: "start",
                os.SEEK_CUR: "offset",
                os.SEEK_END: "end",
            }[__whence]
            raise NotImplementedError(
                0, new_now, self._size, "~", __offset, __whence_str
            )  # TODO
        super().seek(self._start + new_now)
        self._now = new_now
        return self._now

    def read(self, __n: int = -1) -> AnyStr:
        remaining = self._remaining

        if __n == -1:  # Read All
            __n = remaining
        elif __n > remaining:  # Clamp
            __n = remaining

        with self.__rw_ctx():
            return super().read(__n)

    def readline(self, __limit: int = ...) -> AnyStr:
        raise NotImplementedError

    def readlines(self, __limit: int = ...) -> AnyStr:
        raise NotImplementedError

    def write(self, __s: AnyStr) -> int:
        remaining = self._remaining

        if len(__s) > remaining:
            raise RelicToolError(
                f"Cannot write {len(__s)} bytes, only {remaining} bytes remaining!"
            )

        with self.__rw_ctx():
            return super().write(__s)

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        raise NotImplementedError  # TODO


class LazyBinary(BinaryWrapper):
    def __init__(
        self,
        parent: BinaryIO,
        close_parent: bool = False,
        cacheable: Optional[bool] = None,
        name: Optional[str] = None,
    ):
        super().__init__(parent, close_parent=close_parent, name=name)
        if cacheable is None:
            cacheable = "r" in parent.mode

        cache = {} if cacheable else None
        self._cache: Optional[Dict[Tuple[int, int], bytes]] = cache

    def _read_bytes(self, offset: int, size: Optional[int]) -> bytes:
        if size is None:
            size = -1

        def _read():
            self.seek(offset)
            return self.read(size)

        if self._cache is not None:
            key = (offset, size)
            if key in self._cache:
                return self._cache[key]

            value = self._cache[key] = _read()
            return value
        else:
            return _read()

    def _write_bytes(self, b: bytes, offset, size):
        if len(b) > size:
            raise NotImplementedError
        self.seek(offset)
        return self.write(b)

    @classmethod
    def _unpack_str(cls, b: bytes, encoding: str):
        return b.decode(encoding)

    @classmethod
    def _unpack_int(cls, b: bytes, byteorder="little", signed: bool = False) -> int:
        return int.from_bytes(b, byteorder, signed=signed)

    @classmethod
    def __pack_int(
        cls, v: int, length: int, byteorder="little", signed: bool = False
    ) -> bytes:
        return v.to_bytes(length, byteorder, signed=signed)

    @classmethod
    def _unpack_uint16(cls, b: bytes, byteorder="little"):
        return cls._unpack_int(b, byteorder, False)

    @classmethod
    def _pack_uint16(cls, v: int, byteorder="little"):
        return cls.__pack_int(v, 2, byteorder, False)


ByteOrder = Literal["big", "little"]


class BinaryReader:
    def __init__(self, stream: BinaryIO):
        self._stream = stream
        self._cache: Dict[Tuple[int, Optional[int]], Any] = {}

    def _raw_read(self, offset: int, size: int) -> bytes:
        self._stream.seek(offset)
        return self._stream.read(size)

    def read_bytes(self, offset: int, size: Optional[int]) -> bytes:
        if size is None:
            size = -1

        if self._cache is not None:
            key = (offset, size)
            if key in self._cache:
                return self._cache[key]

            value = self._cache[key] = self._raw_read(offset, size)
            return value
        else:
            return self._raw_read(offset, size)

    def _read_int(
        self,
        offset: int,
        size: Optional[int],
        byteorder: ByteOrder,
        signed: bool,
        valid_size: int,
    ):
        size = self._validate_size(size, valid_size)
        buffer = self.read_bytes(offset, size)
        return int.from_bytes(buffer, byteorder=byteorder, signed=signed)

    @staticmethod
    def _validate_size(size: Optional[int], valid: int) -> int:
        if size is None:
            size = valid
        elif size != valid:
            raise ValueError
        return size

    def read_uint8(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=False, valid_size=1
        )

    def read_int8(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=True, valid_size=1
        )

    def read_uint16(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=False, valid_size=2
        )

    def read_int16(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=True, valid_size=2
        )

    def read_uint32(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=False, valid_size=4
        )

    def read_int32(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=True, valid_size=4
        )

    def read_uint64(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=False, valid_size=8
        )

    def read_int64(
        self, offset: int, size: Optional[int] = None, byteorder: ByteOrder = "little"
    ):
        return self._read_int(
            offset, size, byteorder=byteorder, signed=True, valid_size=8
        )


T = TypeVar("T")

_KiB = 1024


class ZLibFileReader(BinaryWrapper):
    def __init__(self, parent: BinaryIO, *, chunk_size: int = 16 * _KiB):
        super().__init__(parent)
        self._data_cache = None
        self._now = 0
        self._chunk_size = chunk_size

    @property
    def _remaining(self):
        return len(self._data) - self._now

    @property
    def _data(self):
        if self._data_cache is None:
            parts = []
            decompressor = zlib.decompressobj()
            while True:
                chunk = self._parent.read(self._chunk_size)
                if len(chunk) == 0:
                    break
                part = decompressor.decompress(chunk)
                parts.append(part)
            last = decompressor.flush()
            parts.append(last)
            self._data_cache = b"".join(parts)
        return self._data_cache

    def read(self, __n: int = -1) -> AnyStr:
        remaining = self._remaining
        size = min(remaining, __n) if __n != -1 else remaining
        buffer = self._data[self._now : self._now + size]
        self._now += size
        return buffer

    def readline(self, __limit: int = -1) -> AnyStr:
        raise NotImplementedError

    def readlines(self, __limit: int = -1) -> AnyStr:
        raise NotImplementedError

    def seek(self, __offset: int, __whence: int = 0) -> int:
        if __whence == os.SEEK_SET:
            new_now = __offset
        elif __whence == os.SEEK_CUR:
            new_now = __offset + self._now
        elif __whence == os.SEEK_END:
            new_now = len(self._data) - __offset
        else:
            raise ValueError(__whence)
        self._now = new_now
        return new_now

    def tell(self) -> int:
        return self._now

    def writable(self) -> bool:
        return False

    def write(self, __s: AnyStr) -> int:
        raise NotImplementedError

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        raise NotImplementedError


class ZLibFile(BinaryWrapper):
    def __init__(self, parent: BinaryIO, *, buffer_size: int = 16 * _KiB):
        super().__init__(parent)
        # self._compressor = zlib.compressobj()
        self._decompressor = zlib.decompressobj()
        self._buffer_size = buffer_size
        self._buffer_index = 0
        self._pos_in_buffer = 0
        self._buffer = None
        self._data = None
        # self._now = 0

    @property
    def _remaining(self):
        return self._buffer_size - self._pos_in_buffer

    def _read_buffer(self):
        self._buffer = super().read(self._buffer_size)
        self._data = self._decompressor.decompress(self._buffer)
        # self._now = self.tell()

    def _read_from_buffer(self, size: int = -1) -> bytes:
        if self._remaining == 0 or self._data is None:
            self._read_buffer()
        if size > self._remaining or size == -1:
            size = self._remaining
        data = self._data[self._pos_in_buffer : self._pos_in_buffer + size]
        self._pos_in_buffer += size
        return data

    def read(self, __n: int = -1) -> bytes:
        parts = []
        if __n == -1:
            while True:
                part = self._read_from_buffer()
                if len(part) == 0 and len(self._decompressor.unconsumed_tail) == 0:
                    break
                parts.append(part)
        else:
            while __n > 0:
                part = self._read_from_buffer(__n)
                if len(part) == 0 and len(self._decompressor.unconsumed_tail) == 0:
                    break
                __n -= len(part)
                parts.append(part)
        return b"".join(parts)

    def seek(self, __offset: int, __whence: int = 0) -> int:
        new_now = super().seek(__offset, __whence)
        buffer_index = new_now // self._buffer_size
        pos_in_buffer = new_now % self._buffer_size

        if buffer_index != self._buffer_index:
            if buffer_index == self._buffer_index + 1:  # Read next buffer
                self._read_buffer()
            else:  # Read from scratch
                self._buffer = self._data = None
                super().seek(0)
                self._decompressor = (
                    zlib.decompressobj()
                )  # have to recreate, according to docs
                for _ in range(buffer_index):
                    self._read_buffer()
        self._pos_in_buffer = pos_in_buffer

        return new_now

    def tell(self) -> int:
        return self._buffer_index * self._buffer_size + self._pos_in_buffer


def tell_end(stream: BinaryIO):
    now = stream.tell()
    end = stream.seek(0, 2)
    stream.seek(now)
    return end
