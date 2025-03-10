"""
Tools for serializing binary data, wrapping binary streams, and lazily reading/writing binary data.
"""

from __future__ import annotations

import math
import os
import zlib
from contextlib import contextmanager
from types import TracebackType
from typing import (
    BinaryIO,
    Type,
    Iterator,
    Iterable,
    Tuple,
    Dict,
    Optional,
    Any,
    Literal,
    Protocol,
    Union,
    runtime_checkable,
    Generator,
    List,
    TypeVar,
    Generic,
)
from collections.abc import Sized
from relic.core.errors import RelicToolError, MismatchError, RelicSerializationSizeError
from relic.core.typeshed import Buffer

ByteOrder = Literal["big", "little"]

_KIBIBYTE = 1024


@runtime_checkable
class BinaryProxy(Protocol):  # pylint: disable=too-few-public-methods
    """
    A Protocol allowing classes to proxy being a BianryIO to lazyio classes
    """

    def __binio_proxy__(self) -> Union[BinaryIO, BinaryProxy]:
        """
        Get the instance this class proxies to

        :returns: The BinaryIO or BinaryProxy that this object proxies to
        :rtype: Union[BinaryIO, BinaryProxy]
        """
        raise NotImplementedError


def is_proxy(s: Any) -> bool:
    """
    Return whether an object is a Binary Proxy

    :rtype: bool
    :returns: True if the object is a BinaryProxy, False otherwise
    """
    return isinstance(s, BinaryProxy)


def get_proxy(s: Union[BinaryProxy, BinaryIO]) -> BinaryIO:
    """
    Resolves a proxy chain recursively

    :rtype: BinaryIO
    :returns: The final BinaryIO instance a BinaryProxy proxies to.
        If the instance is a BianryIO, the instance is returned as is
    """
    if isinstance(s, BinaryProxy):
        proxy = s.__binio_proxy__()
        return get_proxy(proxy)  # resolve nested proxies
    return s


class BinaryWrapper(BinaryIO):
    """
    Allows a BinaryIO object to be wrapped and subclassed without altering the parent BinaryIO object
    """

    def __init__(
        self,
        parent: Union[BinaryProxy, BinaryIO],
        close_parent: bool = True,
        name: Optional[str] = None,
    ):
        self._handle = get_proxy(parent)
        self._close_parent = close_parent
        self._closed = False
        self._name = name

    def __enter__(self) -> BinaryIO:
        return self

    @property
    def name(self) -> str:
        """
        The name of the binary wrapper.

        This will be the name specified in __init__, if given.
        Otherwise, if the underlying handle has a name, the handle's name will be used.
        If neither object has a name, the string representation of the underlying handle is returned.

        :returns: The name of the binary wrapper.
        :rtype: str
        """
        return (
            self._name
            if self._name is not None
            else (
                self._handle.name
                if hasattr(self._handle, "name")
                else str(self._handle)
            )
        )

    def close(self) -> None:
        """
        Closes this object. The underlying file stream is also closed if `close_parent` was True in `__init__`.
        """
        if self._close_parent:
            self._handle.close()
        self._closed = True

    @property
    def closed(self) -> bool:
        """
        Whether this stream is closed.

        If the underlying stream is already closed, this will return True, even if `closed` was not called.
        """
        return self._handle.closed or self._closed

    def fileno(self) -> int:
        "`fileno() on python.org <https://docs.python.org/library/typing.html#typing.IO.fileno>`_"
        return self._handle.fileno()

    def flush(self) -> None:
        "`flush() on python.org <https://docs.python.org/library/typing.html#typing.IO.flush>`_"
        return self._handle.flush()

    def isatty(self) -> bool:
        "`isatty() on python.org <https://docs.python.org/library/typing.html#typing.IO.isatty>`_"
        return self._handle.isatty()

    def read(self, __n: int = -1) -> bytes:
        "`read() on python.org <https://docs.python.org/library/typing.html#typing.IO.read>`_"
        return self._handle.read(__n)

    def readable(self) -> bool:
        "`readable() on python.org <https://docs.python.org/library/typing.html#typing.IO.readable>`_"
        return self._handle.readable()

    def readline(self, __limit: int = -1) -> bytes:
        "`readline() on python.org <https://docs.python.org/library/typing.html#typing.IO.readline>`_"
        return self._handle.readline(__limit)

    def readlines(self, __hint: int = -1) -> list[bytes]:
        "`readlines() on python.org <https://docs.python.org/library/typing.html#typing.IO.readlines>`_"
        return self._handle.readlines(__hint)

    def seek(self, __offset: int, __whence: int = 0) -> int:
        "`seek() on python.org <https://docs.python.org/library/typing.html#typing.IO.seek>`_"
        return self._handle.seek(__offset, __whence)

    def seekable(self) -> bool:
        "`seekable() on python.org <https://docs.python.org/library/typing.html#typing.IO.seekable>`_"
        return self._handle.seekable()

    def tell(self) -> int:
        "`tell() on python.org <https://docs.python.org/library/typing.html#typing.IO.tell>`_"
        return self._handle.tell()

    def truncate(self, __size: Optional[int] = None) -> int:
        "`truncate() on python.org <https://docs.python.org/library/typing.html#typing.IO.truncate>`_"
        return self._handle.truncate(__size)

    def writable(self) -> bool:
        "`writable() on python.org <https://docs.python.org/library/typing.html#typing.IO.writable>`_"
        return self._handle.writable()

    def write(self, __s: Union[bytes, Buffer]) -> int:
        "`write() on python.org <https://docs.python.org/library/typing.html#typing.IO.write>`_"
        return self._handle.write(__s)

    def writelines(self, __lines: Iterable[Union[bytes, Buffer]]) -> None:
        "`writelines() on python.org <https://docs.python.org/library/typing.html#typing.IO.writelines>`_"
        return self._handle.writelines(__lines)

    def __next__(self) -> bytes:
        "`__next__() on python.org <https://docs.python.org/library/typing.html#typing.IO.__next__>`_"
        return self._handle.__next__()

    def __iter__(self) -> Iterator[bytes]:
        "`__iter__() on python.org <https://docs.python.org/library/typing.html#typing.IO.__iter__>`_"
        return self._handle.__iter__()

    def __exit__(
        self,
        __t: Type[BaseException] | None,
        __value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> None:
        "`__exit__() on python.org <https://docs.python.org/library/typing.html#typing.IO.__exit__>`_"
        # TODO, this may fail to close the file if an err is thrown
        if self._close_parent:
            self._handle.__exit__(__t, __value, __traceback)

    @property
    def mode(self) -> str:
        """
        The Mode of the underlying stream; if the underlying stream does not specify a mode, it is determined as follow.
        If the underlying stream is readable and writeable, 'w+b' is returned.
        If the underlying stream is only readable, 'rb' is returned.
        If the underlying stream is only writable, 'wb' is returned.
        Otherwise, raises a RelicToolError.

        :raises RelicToolError: The mode could not be determined automatically.

        :returns: The mode the stream was created with.
        :rtype: str
        """

        if hasattr(self._handle, "mode"):
            return self._handle.mode

        readable = self.readable()
        writable = self.writable()

        if readable and writable:
            return r"w+b"
        if readable:
            return r"rb"
        if writable:
            return r"wb"

        raise RelicToolError(
            "Binary Wrapper could not determine mode for object that is not readable or writeable;"
            " the IO object may not be supported."
        )


class BinaryWindow(BinaryWrapper):
    """
    A BinaryIO which only exposes a 'slice' of the stream

    Maintains an internal pointer to the current position of the window, ignoring the parent stream's current position
    """

    def __init__(  # pylint: disable=R0917
        self,
        parent: Union[BinaryIO, BinaryProxy],
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
    def __rw_ctx(self) -> Generator[None, None, None]:
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
            raise RelicToolError("Invalid Seek: seeking past start of stream!")
        super().seek(self._start + new_now)
        self._now = new_now
        return self._now

    def read(self, __n: int = -1) -> bytes:
        remaining = self._remaining

        if __n == -1:  # Read All
            __n = remaining
        elif __n > remaining:  # Clamp
            __n = remaining

        with self.__rw_ctx():
            return super().read(__n)

    def readline(self, __limit: int = ...) -> bytes:
        raise NotImplementedError

    def readlines(self, __limit: int = ...) -> List[bytes]:
        raise NotImplementedError

    def write(self, __s: Union[bytes, Buffer]) -> int:
        remaining = self._remaining

        if isinstance(__s, Sized) and len(__s) > remaining:
            raise RelicToolError(
                f"Cannot write {len(__s)} bytes, only {remaining} bytes remaining!"
            )

        with self.__rw_ctx():
            return super().write(__s)

    def writelines(self, __lines: Iterable[Union[bytes, Buffer]]) -> None:
        raise NotImplementedError


class _CStringOps:
    """
    Provides utility functions for serializing C-String Buffers.
    """

    def __init__(self, serialzer: BinarySerializer):
        self._serializer = serialzer

    def read(
        self,
        offset: int,
        size: int,
        *,
        encoding: str,
        padding: Optional[str] = None,
        exact_size: bool = True,
    ) -> str:
        buffer = self._serializer.read_bytes(offset, size, exact_size=exact_size)
        result = self.unpack(buffer, encoding=encoding, padding=padding)
        return result

    def write(
        self,
        value: str,
        offset: int,
        size: int,
        *,
        encoding: str,
        padding: Optional[str] = None,
    ) -> int:
        buffer = self.pack(value, encoding=encoding, size=size, padding=padding)
        return self._serializer.write_bytes(buffer, offset, size)

    @classmethod
    def unpack(cls, b: bytes, encoding: str, padding: Optional[str] = None) -> str:
        value: str = b.decode(encoding)
        if padding is not None:
            value = value.strip(padding)
        return value

    @classmethod
    def pack(
        cls,
        v: str,
        encoding: str,
        size: Optional[int] = None,
        padding: Optional[str] = None,
    ) -> bytes:
        buffer = v.encode(encoding)
        if size is not None:
            if len(buffer) < size and padding is not None and len(padding) > 0:
                pad_buffer = padding.encode(encoding)
                pad_count = (size - len(buffer)) / len(pad_buffer)
                if pad_count != int(pad_count):
                    raise RelicToolError(
                        f"Trying to pad '{buffer!r}' ({len(buffer)}) to '{size}' bytes,"
                        f" but padding '{pad_buffer!r}' ({len(pad_buffer)})"
                        f" is not a multiple of '{size - len(buffer)}' !"
                    )
                buffer = b"".join([buffer, pad_buffer * int(pad_count)])
            elif len(buffer) != size:
                raise MismatchError("Writing Bytes", len(buffer), size)
        return buffer


class _IntOps:
    """
    Provides utility functions for serializing Any Integer

    Provides more dynamic read/writes at the expense of less validity checks than _SizedIntOps
    """

    def __init__(self, serialzer: BinarySerializer):
        self._serializer = serialzer

    def read(
        self,
        offset: int,
        size: Optional[int] = None,
        *,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> int:
        if size is None:
            raise RelicToolError(
                "Cannot dynamically determine size of the int buffer;"
                " please specify the size manually or use a sized int reader"
            )
        buffer = self._serializer.read_bytes(offset, size, exact_size=True)
        result = self.unpack_int(
            buffer, length=size, byteorder=byteorder, signed=signed
        )
        return result

    def write(
        self,
        value: int,
        offset: int,
        size: Optional[int] = None,
        *,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> int:
        if size is None:
            raise RelicToolError(
                "Cannot dynamically determine size of the int buffer;"
                " please specify the size manually or use a sized int writer"
            )
        buffer = self.pack_int(value, byteorder=byteorder, length=size, signed=signed)
        return self._serializer.write_bytes(buffer, offset, size)

    @staticmethod
    def unpack_int(
        b: bytes,
        length: Optional[int],
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> int:
        if length is not None and len(b) != length:
            raise MismatchError("Buffer Size", len(b), length)
        return int.from_bytes(b, byteorder, signed=signed)

    @staticmethod
    def pack_int(
        v: int,
        length: int,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> bytes:
        return v.to_bytes(length, byteorder, signed=signed)


class _SizedIntOps(_IntOps):
    """
    Provides utility functions for serializing Sized & Signed Integers

    Provides more validation over input/output then _IntOps
    """

    def __init__(self, serializer: BinarySerializer, size: int, signed: bool):
        super().__init__(serializer)
        self._size = size
        self._signed = signed

    def _validate_args(
        self, size: Optional[int], signed: Optional[bool] = None
    ) -> None:
        received_size = size if size is not None else self._size
        received_signed = signed if signed is not None else self._signed

        expected = f"{'' if self._signed else 'U'}Int-{self._size * 8}"
        received = f"{'' if received_signed else 'U'}Int-{received_size * 8}"
        if expected != received:
            raise MismatchError("Int Type", received, expected)

    def read(
        self,
        offset: int,
        size: Optional[int] = None,
        *,
        byteorder: Literal["little", "big"] = "little",
        signed: Optional[bool] = None,
    ) -> int:
        self._validate_args(size, signed)
        buffer = self._serializer.read_bytes(offset, self._size, exact_size=True)
        result = self.unpack(buffer, byteorder=byteorder, signed=self._signed)
        return result

    def write(
        self,
        value: int,
        offset: int,
        size: Optional[int] = None,
        *,
        byteorder: Literal["little", "big"] = "little",
        signed: Optional[bool] = None,
    ) -> int:
        self._validate_args(size, signed)
        buffer = self.pack(
            value, byteorder=byteorder, length=self._size, signed=self._signed
        )
        return self._serializer.write_bytes(buffer, offset, size)

    def read_le(self, offset: int, size: Optional[int] = None) -> int:
        """Read little endian integer"""
        return self.read(offset=offset, size=size, byteorder="little")

    def write_le(self, value: int, offset: int, size: Optional[int] = None) -> int:
        """Write little endian integer"""
        return self.write(value=value, offset=offset, size=size, byteorder="little")

    def read_be(self, offset: int, size: Optional[int] = None) -> int:
        """Read big endian integer"""
        return self.read(offset=offset, size=size, byteorder="big")

    def write_be(self, value: int, offset: int, size: Optional[int] = None) -> int:
        """Write big endian integer"""
        return self.write(value=value, offset=offset, size=size, byteorder="big")

    def unpack(
        self,
        data: bytes,
        length: Optional[int] = None,
        byteorder: Literal["little", "big"] = "little",
        signed: Optional[bool] = None,
    ) -> int:
        self._validate_args(length, signed)
        return int.from_bytes(data, byteorder=byteorder, signed=self._signed)

    def pack(
        self,
        value: int,
        length: Optional[int] = None,
        byteorder: Literal["little", "big"] = "little",
        signed: Optional[bool] = None,
    ) -> bytes:
        """
        Pack an integer into a C-like binary buffer

        :param value: The value to pack.
        :type value: int

        :param length: The length in bytes that the value should be packed into.
            Raises an error if it is not None and does not match the class definition.
        :type length: int, optional

        :param byteorder: The byteorder or 'endianness' of the buffer. By default, "little"
        :type byteorder: Literal["little", "big"], optional

        :param signed: Whether the integer should be packed as a signed or unsigned integer.
            Raises an error if it is not None and does not match the class definition.

        :raises MismatchError: The length or signed parameter does not match the class's size/signed value(s).

        """

        self._validate_args(length, signed)
        return value.to_bytes(self._size, byteorder=byteorder, signed=self._signed)


class BinarySerializer(BinaryProxy):  # pylint: disable= too-many-instance-attributes
    """
    A utility object that allows serializing/deserializing most data types

    Acts as a BinaryProxy which points to the parent object it reads from/writes to
    """

    def __init__(
        self,
        parent: Union[BinaryIO, BinaryProxy],
        close_parent: bool = False,
        cacheable: Optional[bool] = None,
    ):
        self._proxy = parent
        self._close = close_parent
        if cacheable is None:
            handle = get_proxy(parent)
            cacheable = handle.readable() and not handle.writable()

        self._cache: Optional[Dict[Tuple[int, int], bytes]] = {} if cacheable else None

        self.c_string = _CStringOps(self)
        self.int = _IntOps(self)

        self.uint16 = _SizedIntOps(self, 2, signed=False)
        self.int16 = _SizedIntOps(self, 2, signed=True)

        self.uint32 = _SizedIntOps(self, 4, signed=False)
        self.int32 = _SizedIntOps(self, 4, signed=True)

    def __binio_proxy__(self) -> Union[BinaryIO, BinaryProxy]:
        return self._proxy

    @property
    def stream(self) -> BinaryIO:
        """
        Get the actual stream instance to use as the underlying stream
        """
        return get_proxy(self._proxy)

    # Bytes
    def read_bytes(self, offset: int, size: int, *, exact_size: bool = True) -> bytes:
        """
        Read bytes from the underlying stream.

        :param offset: The offset to read from the underlying stream.
        :type offset: int

        :param size: The number of bytes to read.
        :type size: int

        :param exact_size: If True, the number of bytes read from the stream must match the size parameter.
            By default, True.
        :type exact_size: bool, optional

        :rtype: bytes
        :returns: The bytes read from the underlying stream
        """

        def _read() -> bytes:
            self.stream.seek(offset)
            b = self.stream.read(size)
            if exact_size and len(b) != size:
                raise MismatchError("Read Mismatch", len(b), size)
            return b

        if self._cache is not None:
            key = (offset, size)
            if key in self._cache:
                return self._cache[key]
            value = self._cache[key] = _read()
            return value

        return _read()

    def write_bytes(self, data: bytes, offset: int, size: Optional[int] = None) -> int:
        """
        Writes a byte buffer to the underlying stream.

        :param data: The byte buffer to write to the stream.
        :type data: bytes

        :param offset: The position from the start of the underlying stream to write to
        :type offset: int

        :param size: The expected size of the byte-buffer. By default, none.
        :type size: Optional[int], optional

        :raises MismatchError: The data buffer did not match the given size.
        """
        if size is not None and len(data) != size:
            raise MismatchError("Write Mismatch", len(data), size)
        self.stream.seek(offset)
        return self.stream.write(data)


class BinaryProxySerializer(BinaryProxy):  # pylint: disable= R0903
    """
    A Mixin-like class which allows the class to be treated as a BinaryIO via proxying,
     and automatically creates a serializer to be used to read/write data lazily
    """

    def __init__(
        self,
        stream: Union[BinaryIO, BinaryProxy],
    ):
        self._serializer = BinarySerializer(stream)

    def __binio_proxy__(self) -> Union[BinaryIO, BinaryProxy]:
        return self._serializer


class ZLibFileReader(BinaryWrapper):
    """
    A wrapper which lazily reads a Z-Lib compressed file.
    """

    def __init__(
        self, parent: Union[BinaryIO, BinaryProxy], *, chunk_size: int = 16 * _KIBIBYTE
    ):
        super().__init__(parent)
        self._data_cache: Optional[bytes] = None
        self._now = 0
        self._chunk_size = chunk_size

    @property
    def _remaining(self) -> int:
        return len(self._data) - self._now

    @property
    def _data(self) -> bytes:
        if self._data_cache is None:
            parts = []
            decompressor = zlib.decompressobj()
            while True:
                chunk = self._handle.read(self._chunk_size)
                if len(chunk) == 0:
                    break
                part = decompressor.decompress(chunk)
                parts.append(part)
            last = decompressor.flush()
            parts.append(last)
            self._data_cache = b"".join(parts)
        return self._data_cache

    def read(self, __n: int = -1) -> bytes:
        remaining = self._remaining
        size = min(remaining, __n) if __n != -1 else remaining
        buffer = self._data[self._now : self._now + size]
        self._now += size
        return buffer

    def readline(self, __limit: int = -1) -> bytes:
        raise NotImplementedError

    def readlines(self, __limit: int = -1) -> List[bytes]:
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

    def write(self, __s: Union[bytes, Buffer]) -> int:
        raise NotImplementedError

    def writelines(self, __lines: Iterable[Union[bytes, Buffer]]) -> None:
        raise NotImplementedError


def tell_end(stream: BinaryIO) -> int:
    """
    Gets the index of the end of the stream; unless written to further, this will be the size of the stream
    :param stream: The stream to get the end of

    :returns: The index of the last position in the stream
    :rtype: int
    """
    now = stream.tell()
    end = stream.seek(0, os.SEEK_END)
    stream.seek(now)
    return end


def read_chunks(
    stream: Union[BinaryIO, bytes, bytearray],
    start: Optional[int] = None,
    size: Optional[int] = None,
    chunk_size: int = _KIBIBYTE * 16,
) -> Iterable[bytes]:
    """
    Yields chunks from the stream until the size or the end of the stream is reached

    :param stream: The bytes-like to read from
    :type stream: Union[BinaryIO, bytes, bytearray]

    :param start: The offset to start reading from,
        if None the current position is used (BinaryIO) or the start of the buffer (bytes / bytearray).
        By default, this is None
    :type start: Optional[int], optional

    :param size: The maximum number of bytes to read,
        if None, all bytes will be read.
        By default, this is None
    :type size: Optional[int], optional

    :param chunk_size: The maximum number of bytes to yield at a time.
        By default, this is 16 KiB
    :type chunk_size: int

    :returns: An iterable of bytes containing all data from start to start + size
    :rtype: Iterable[bytes]
    """

    if isinstance(stream, (bytes, bytearray)):
        if start is None:
            start = 0
        if size is None:
            size = len(stream) - start
        for index in range(math.ceil(size / chunk_size)):
            read_start = start + index * chunk_size
            read_end = start + min((index + 1) * chunk_size, size)
            yield stream[read_start:read_end]
    else:
        if start is not None:
            stream.seek(start)
        if size is None:
            while True:
                buffer = stream.read(chunk_size)
                if len(buffer) == 0:
                    return
                yield buffer
        else:
            while size > 0:
                buffer = stream.read(min(size, chunk_size))
                size -= len(buffer)
                if len(buffer) == 0:
                    return
                yield buffer


def chunk_copy(  # pylint: disable=R0917
    src: Union[BinaryIO, bytes, bytearray],
    dest: Union[BinaryIO, bytearray],
    src_start: Optional[int] = None,
    size: Optional[int] = None,
    dst_start: Optional[int] = None,
    chunk_size: int = _KIBIBYTE * 16,
) -> None:
    """
    Copies from a source bytes-like to a destination bytes-like in chunks.

    :param src: The source bytes-like
    :type src: Union[BinaryIO, bytes, bytearray]

    :param dest: The destination bytes-like
    :type dest: Union[BinaryIO, bytearray]

    :param src_start: The starting offset to read from the source,
        defaults to the current position of the stream (BinaryIO) or the start of the buffer (bytes/bytearray)
    :type src_start: Optional[int], optional

    :param size: The amount of bytes to read from the source,
        if not specified, will read all bytes possible
    :type size: Optional[int], optional

    :param dst_start: The starting offset to write to the destination,
        defaults to the current position of the stream (BinaryIO) or the start of the buffer (bytearray)
    :type dst_start: Optional[int], optional

    :param chunk_size: The number of bytes to copy from the source to the destination in a single step;
        by default this is 16 KiB
    :type chunk_size: int, optional

    """
    if isinstance(dest, bytearray):
        if src_start is None:
            src_start = 0
        if dst_start is None:
            dst_start = 0

        for i, chunk in enumerate(read_chunks(src, src_start, size, chunk_size)):
            chunk_offset = i * chunk_size
            chunk_size = len(chunk)
            dest[dst_start + chunk_offset : dst_start + chunk_offset + chunk_size] = (
                chunk
            )
    elif isinstance(dest, bytes):
        raise RelicToolError("Cannot chunk copy to a bytes object!")
    else:
        if dst_start is not None:
            dest.seek(dst_start)
        for chunk in read_chunks(src, src_start, size, chunk_size):
            dest.write(chunk)


_T = TypeVar("_T")


class BinaryConverter(Protocol[_T]):
    def bytes2value(self, b: bytes) -> _T:
        raise NotImplementedError

    def value2bytes(self, v: _T) -> bytes:
        raise NotImplementedError


class ByteConverter(BinaryConverter[bytes]):
    @classmethod
    def bytes2value(cls, b: bytes) -> bytes:  # pylint: disable=W0221
        return b

    @classmethod
    def value2bytes(cls, v: bytes) -> bytes:  # pylint: disable=W0221
        return v


class IntConverter(BinaryConverter[int]):
    def __init__(
        self,
        length: int,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ):
        self._length = length
        self._byteorder = byteorder
        self._signed = signed

    def bytes2value(self, b: bytes) -> int:
        if len(b) != self._length:
            raise RelicSerializationSizeError(
                f"`{b!r}` expected '{self._length}' bytes, got '{len(b)}' bytes"
            )
        return int.from_bytes(b, self._byteorder, signed=self._signed)

    def value2bytes(self, v: int) -> bytes:
        return int.to_bytes(v, self._length, self._byteorder, signed=self._signed)


class CStringConverter(BinaryConverter[str]):
    def __init__(
        self,
        encoding: str = "ascii",
        padding: Optional[str] = None,
        size: Optional[int] = None,
    ):
        self._encoding = encoding
        self._padding = padding
        self._size = size

    def bytes2value(self, b: bytes) -> str:
        if self._size is not None and len(b) != self._size:
            raise RelicSerializationSizeError(
                f"`{b!r}` expected '{self._size}' bytes, got '{len(b)}' bytes"
            )
        decoded = b.decode(self._encoding)

        if self._padding is not None:
            unpadded = decoded.rstrip(self._padding)
        else:
            unpadded = decoded

        return unpadded

    def value2bytes(self, v: str) -> bytes:
        encoded = v.encode(self._encoding)

        if self._size is not None and len(encoded) != self._size:
            if self._padding is None:
                raise RelicToolError("CString Converter")

            _padding = self._padding.encode(self._encoding)
            pad_size = (self._size - len(encoded)) / len(_padding)
            if int(pad_size) != pad_size:
                raise RelicToolError("CString Converter")
            padding = _padding * int(pad_size)
        else:
            padding = b""

        padded = encoded + padding
        return padded


class BinaryProperty(Generic[_T]):
    """
    Helper class to convert binary data to typed data as a lazy property
    Expect a BinaryIO '_serializer' object on the parent object
    """

    def __init__(self, start: int, size: int, converter: BinaryConverter[_T]):
        self._start = start
        self._size = size
        self._converter = converter

    def __get__(self, instance: Any, owner: Any) -> _T:
        serializer = instance._serializer
        buffer = self._read(serializer)
        value = self._converter.bytes2value(buffer)
        return value

    def __set__(self, instance: Any, value: _T) -> None:
        serializer = instance._serializer
        buffer = self._converter.value2bytes(value)
        self._write(serializer, buffer)

    @contextmanager
    def _window(self, stream: BinaryIO) -> Generator[BinaryIO, None, None]:
        """Open a window into the stream from the expected start and end of this data's location"""
        yield BinaryWindow(stream, self._start, self._size)

    def _read(self, stream: BinaryIO) -> bytes:
        """Read a byte buffer from the given stream"""
        with self._window(stream) as window:
            return window.read()

    def _write(self, stream: BinaryIO, value: bytes) -> None:
        """Write the byte buffer to the given stream"""
        with self._window(stream) as window:
            window.write(value)


class ConstProperty(Generic[_T]):
    """
    A property for a contsant value
    Raises an error if a new constant is set
    """

    def __init__(self, value: _T, err: Exception):
        self._value = value
        self._err = err

    def __get__(self, instance: Any, owner: Any) -> _T:
        return self._value

    def __set__(self, instance: Any, value: _T) -> None:
        raise self._err
