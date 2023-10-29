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
    TypeVar,
    Any,
    Literal,
    Protocol,
    Union,
    runtime_checkable,
    Generator,
    List,
)

from relic.core.typeshed import Buffer
from relic.core.errors import RelicToolError


@runtime_checkable
class BinaryProxy(Protocol):  # pylint: disable=too-few-public-methods
    def __binio_proxy__(self) -> Union[BinaryIO, BinaryProxy]:
        raise NotImplementedError


def is_proxy(s: Any) -> bool:
    return isinstance(s, BinaryProxy)


def get_proxy(s: Union[BinaryProxy, BinaryIO]) -> BinaryIO:
    if isinstance(s, BinaryProxy):
        proxy = s.__binio_proxy__()
        return get_proxy(proxy)  # resolve nested proxies
    return s


class BinaryWrapper(BinaryIO):
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
        return self._name or (
            self._handle.name if hasattr(self._handle, "name") else str(self._handle)
        )

    def close(self) -> None:
        if self._close_parent:
            self._handle.close()
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._handle.closed or self._closed

    def fileno(self) -> int:
        return self._handle.fileno()

    def flush(self) -> None:
        return self._handle.flush()

    def isatty(self) -> bool:
        return self._handle.isatty()

    def read(self, __n: int = -1) -> bytes:
        return self._handle.read(__n)

    def readable(self) -> bool:
        return self._handle.readable()

    def readline(self, __limit: int = -1) -> bytes:
        return self._handle.readline(__limit)

    def readlines(self, __hint: int = -1) -> list[bytes]:
        return self._handle.readlines(__hint)

    def seek(self, __offset: int, __whence: int = 0) -> int:
        return self._handle.seek(__offset, __whence)

    def seekable(self) -> bool:
        return self._handle.seekable()

    def tell(self) -> int:
        return self._handle.tell()

    def truncate(self, __size: Optional[int] = None) -> int:
        return self._handle.truncate(__size)

    def writable(self) -> bool:
        return self._handle.writable()

    def write(self, __s: Union[bytes, Buffer]) -> int:
        return self._handle.write(__s)

    def writelines(self, __lines: Iterable[Union[bytes, Buffer]]) -> None:
        return self._handle.writelines(__lines)

    def __next__(self) -> bytes:
        return self._handle.__next__()

    def __iter__(self) -> Iterator[bytes]:
        return self._handle.__iter__()

    def __exit__(
        self,
        __t: Type[BaseException] | None,
        __value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> None:
        # TODO, this may fail to close the file if an err is thrown
        if self._close_parent:
            self._handle.__exit__(__t, __value, __traceback)

    @property
    def mode(self) -> str:
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
            "Binary Wrapper could not determine mode for object that is not readable or writeable; the IO object may not be supported."
        )


class BinaryWindow(BinaryWrapper):
    def __init__(
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

        if len(__s) > remaining:  # type: ignore[arg-type]
            raise RelicToolError(
                f"Cannot write {len(__s)} bytes, only {remaining} bytes remaining!"  # type: ignore[arg-type]
            )

        with self.__rw_ctx():
            return super().write(__s)

    def writelines(self, __lines: Iterable[Union[bytes, Buffer]]) -> None:
        raise NotImplementedError


class _CStringOps:
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
                        f"Trying to pad '{buffer!r}' ({len(buffer)}) to '{size}' bytes, but padding '{pad_buffer!r}' ({len(pad_buffer)}) is not a multiple of '{size-len(buffer)}' !"
                    )
                buffer = b"".join([buffer, pad_buffer * int(pad_count)])
            elif len(buffer) != size:
                raise RelicToolError(
                    f"Trying to write '{size}' bytes, received '{buffer!r}' ({len(buffer)})!"
                )
        return buffer


class _IntOps:
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
                "Cannot dynamically determine size of the int buffer; please specify the size manually or use a sized int reader"
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
                "Cannot dynamically determine size of the int buffer; please specify the size manually or use a sized int writer"
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
            raise RelicToolError(
                f"Size mismatch, unpacking '{b!r}' got ({len(b)}) bytes but expected ({length}) bytes."
            )
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
    def __init__(self, serialzer: BinarySerializer, size: int, signed: bool):
        super().__init__(serialzer)
        self._size = size
        self._signed = signed

    def _validate_args(self, size: Optional[int], signed: bool) -> None:
        recieved_size = size if size is not None else self._size

        expected = f"{'' if self._signed else 'U'}Int-{self._size * 8}"
        recieved = f"{'' if self._signed else 'U'}Int-{recieved_size * 8}"
        if size is not None and size != self._size:
            raise RelicToolError(
                f"Size mismatch! Expecting a '{expected}' but receiving a '{recieved}'!"
            )
        if signed != self._signed:
            raise RelicToolError(
                f"Signed mismatch! Expecting a '{expected}' but receiving a '{recieved}'!"
            )

    def read(
        self,
        offset: int,
        size: Optional[int] = None,
        *,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
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
        signed: bool = False,
    ) -> int:
        self._validate_args(size, signed)
        buffer = self.pack(
            value, byteorder=byteorder, length=self._size, signed=self._signed
        )
        return self._serializer.write_bytes(buffer, offset, size)

    def read_le(self, offset: int, size: Optional[int] = None) -> int:
        return self.read(offset=offset, size=size, byteorder="little")

    def write_le(self, value: int, offset: int, size: Optional[int] = None) -> int:
        return self.write(value=value, offset=offset, size=size, byteorder="little")

    def read_be(self, offset: int, size: Optional[int] = None) -> int:
        return self.read(offset=offset, size=size, byteorder="big")

    def write_be(self, value: int, offset: int, size: Optional[int] = None) -> int:
        return self.write(value=value, offset=offset, size=size, byteorder="big")

    def unpack(
        self,
        b: bytes,
        length: Optional[int] = None,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> int:
        self._validate_args(length, signed)
        return int.from_bytes(b, byteorder=byteorder, signed=self._signed)

    def pack(
        self,
        v: int,
        length: Optional[int] = None,
        byteorder: Literal["little", "big"] = "little",
        signed: bool = False,
    ) -> bytes:
        self._validate_args(length, signed)
        return v.to_bytes(self._size, byteorder=byteorder, signed=self._signed)


class BinarySerializer(BinaryProxy):  # pylint: disable= too-many-instance-attributes
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
        return get_proxy(self._proxy)

    # Bytes
    def read_bytes(self, offset: int, size: int, *, exact_size: bool = True) -> bytes:
        def _read() -> bytes:
            self.stream.seek(offset)
            b = self.stream.read(size)
            if exact_size and len(b) != size:
                raise RelicToolError(
                    f"Trying to read '{size}' bytes, received '{b!r}' ({len(b)})!"
                )
            return b

        if self._cache is not None:
            key = (offset, size)
            if key in self._cache:
                return self._cache[key]
            value = self._cache[key] = _read()
            return value

        return _read()

    def write_bytes(self, b: bytes, offset: int, size: Optional[int] = None) -> int:
        if size is not None and len(b) != size:
            raise RelicToolError(
                f"Trying to write '{size}' bytes, received '{b!r}' ({len(b)})!"
            )
        self.stream.seek(offset)
        return self.stream.write(b)


class BinaryProxySerializer(BinaryProxy):  # pylint: disable= R0903
    def __init__(
        self,
        stream: Union[BinaryIO, BinaryProxy],
    ):
        self._serializer = BinarySerializer(stream)

    def __binio_proxy__(self) -> Union[BinaryIO, BinaryProxy]:
        return self._serializer


ByteOrder = Literal["big", "little"]


T = TypeVar("T")

_KILOBYTE = 1024


class ZLibFileReader(BinaryWrapper):
    def __init__(
        self, parent: Union[BinaryIO, BinaryProxy], *, chunk_size: int = 16 * _KILOBYTE
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
    now = stream.tell()
    end = stream.seek(0, os.SEEK_END)
    stream.seek(now)
    return end


def read_chunks(
    stream: Union[BinaryIO, bytes, bytearray],
    start: Optional[int] = None,
    size: Optional[int] = None,
    chunk_size: int = _KILOBYTE * 16,
) -> Iterable[bytes]:
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


def chunk_copy(
    src: Union[BinaryIO, bytes, bytearray],
    dest: Union[BinaryIO, bytearray],
    src_start: Optional[int] = None,
    size: Optional[int] = None,
    dst_start: Optional[int] = None,
    chunk_size: int = _KILOBYTE * 16,
) -> None:
    if isinstance(dest, bytearray):
        if src_start is None:
            src_start = 0
        if dst_start is None:
            dst_start = 0

        for i, chunk in enumerate(read_chunks(src, src_start, size, chunk_size)):
            chunk_offset = i * chunk_size
            chunk_size = len(chunk)
            dest[
                dst_start + chunk_offset : dst_start + chunk_offset + chunk_size
            ] = chunk
    elif isinstance(dest, bytes):
        raise RelicToolError("Cannot chunk copy to a bytes object!")
    else:
        if dst_start is not None:
            dest.seek(dst_start)
        for chunk in read_chunks(src, src_start, size, chunk_size):
            dest.write(chunk)
