import contextlib
import os
import zlib
from io import BytesIO
from typing import BinaryIO, Optional, Any, Tuple, TypeVar, Type

import pytest

from relic.core.errors import RelicSerializationSizeError, RelicToolError
from relic.core.lazyio import (
    BinaryWrapper,
    BinarySerializer,
    BinaryWindow,
    ConstProperty,
    BinaryProperty,
    BinaryConverter,
    CStringConverter,
    IntConverter,
    ByteConverter,
    BinaryProxySerializer,
    chunk_copy,
    read_chunks,
    get_proxy,
    tell_end,
    ZLibFileReader,
)

_TestBinaryWrapper_AutoNamed = [BytesIO()]


class TestBinaryWrapper:
    @pytest.mark.parametrize(
        ["stream", "name"],
        [
            (BinaryWrapper(BytesIO(), name="Bradley"), "Bradley"),
            (BinaryWindow(BytesIO(), 0, 0, name="Steven"), "Steven"),
            *((stream, str(stream)) for stream in _TestBinaryWrapper_AutoNamed),
        ],
    )
    def test_name(self, stream: BinaryIO, name: str):
        with BinaryWrapper(stream) as wrapper:
            assert wrapper.name == name


class TestBinaryWindow:
    @pytest.mark.parametrize(
        ["stream", "buffer", "start", "size"],
        [
            (BinaryWrapper(BytesIO(b"Hal Jordan")), b"Hal", 0, 3),
            (
                BinaryWindow(BinaryWrapper(BytesIO(b"NotAnERROR")), 0, 10),
                b"ERROR",
                5,
                5,
            ),
            (BytesIO(b"Jessabell"), b"bell", 5, 4),
            (BinaryWindow(BytesIO(b"HaveANiceDay"), 5, 4), b"Nice", 0, 4),
        ],
    )
    def test_read(self, stream: BinaryIO, buffer: bytes, start: int, size: int):
        with BinaryWindow(stream, start, size) as window:
            read = window.read()
            assert read == buffer

    @pytest.mark.parametrize(
        ["stream", "buffer", "start", "size", "parent_buffer"],
        [
            (BinaryWrapper(BytesIO(b"Hal Jordan")), b"Dad", 0, 3, b"Dad Jordan"),
            (
                BinaryWindow(BinaryWrapper(BytesIO(b"NotAnERROR")), 0, 10),
                b"Apple",
                5,
                5,
                b"NotAnApple",
            ),
            (BytesIO(b"Jessabell"), b"ball", 5, 4, b"Jessaball"),
            (BinaryWindow(BytesIO(b"HaveANiceDay"), 5, 9), b"Crap", 0, 4, b"CrapDay"),
        ],
    )
    def test_write(
        self,
        stream: BinaryIO,
        buffer: bytes,
        start: int,
        size: int,
        parent_buffer: bytes,
    ):
        with BinaryWindow(stream, start, size) as window:
            window.write(buffer)
        stream.seek(0)
        read = stream.read()
        assert read == parent_buffer


T = TypeVar("T")


@pytest.mark.parametrize(
    ["value", "buffer", "ptr", "converter", "read_err", "write_err"],
    [
        ("Dawn of War", b"\0Dawn of War", (1, 11), CStringConverter(), None, None),
        (
            "Dawn of War II",
            b"\0Dawn of War II\1",
            (1, 15),
            CStringConverter(padding="\1", size=15),
            None,
            None,
        ),
        (
            "Dawn of War III",
            b"\0Dawn of War III",
            (1, 15),
            CStringConverter(padding="", size=14),
            RelicSerializationSizeError,
            RelicToolError,
        ),
        (
            "Dawn of War III",
            b"\0Dawn of War III",
            (1, 15),
            CStringConverter(size=14),
            RelicSerializationSizeError,
            RelicToolError,
        ),
        (
            "Dawn of War III",
            b"\0Dawn of War III",
            (1, 15),
            CStringConverter(padding="\1\2\3", size=14),
            RelicSerializationSizeError,
            RelicToolError,
        ),
        (920, b"\0\0\x98\x03", (2, 2), IntConverter(2, "little", True), None, None),
        (
            920,
            b"\0\0\x98\x03\0\0",
            (2, 2),
            IntConverter(4, "little", True),
            RelicSerializationSizeError,
            RelicToolError,
        ),
        (b"\xde\xad", b"\0\xde\xad\0", (1, 2), ByteConverter, None, None),
    ],
)
class TestBinaryProperty:

    @classmethod
    @contextlib.contextmanager
    def get_serializer(cls, buffer: bytes) -> Any:
        with BytesIO(buffer) as stream:
            yield BinaryProxySerializer(stream)

    def test_get(
        self,
        value: T,
        buffer: bytes,
        ptr: Tuple[int, int],
        converter: BinaryConverter[T],
        write_err: Any,
        read_err: Optional[Type[Exception]],
    ):
        err = read_err
        with self.get_serializer(buffer) as inst:
            property = BinaryProperty(ptr[0], ptr[1], converter)
            try:
                assert property.__get__(inst, None) == value
            except Exception as e:
                if not err:
                    raise
                else:
                    assert isinstance(e, err)

    def test_set(
        self,
        value: T,
        buffer: bytes,
        ptr: Tuple[int, int],
        converter: BinaryConverter[T],
        read_err: Any,
        write_err: Optional[Type[Exception]],
    ):
        err = write_err
        with self.get_serializer(b"\0" * len(buffer)) as inst:
            property = BinaryProperty(ptr[0], ptr[1], converter)
            try:
                property.__set__(inst, value)
            except Exception as e:
                if not err:
                    raise
                else:
                    assert isinstance(e, err)
            else:
                proxy = get_proxy(inst._serializer)
                proxy.seek(0)
                read = proxy.read()
                assert read == buffer


@pytest.mark.parametrize(
    ["value", "err"], [(4, ValueError("Blah")), ("Rugrats", TypeError("Pickles"))]
)
class TestConstProperty:
    def test_get(self, value: Any, err: Exception):
        property = ConstProperty(value, err)
        assert property.__get__(None, None) == value

    def test_set(self, value: Any, err: Exception):
        property = ConstProperty(value, err)
        try:
            property.__set__(None, value)
        except Exception as e:
            assert e == err
        else:
            pytest.fail("Const Property should have raised err when writing")


@contextlib.contextmanager
def opt_stream(buf: bytes | bytearray, is_stream: bool):
    if is_stream:
        with BytesIO(buf) as h:
            yield h
    else:
        yield buf


@pytest.mark.parametrize(
    [
        "src",
        "dest",
        "src_start",
        "size",
        "dest_start",
        "src_is_stream",
        "dest_is_stream",
        "err",
    ],
    [
        (b"\1deadbeef", b"\0deadbeef", 1, 8, 1, False, False, RelicToolError),
        (b"\1deadbeef", bytearray(b"\0deadbeef"), 1, 8, 1, False, False, None),
        (b"\1deadbeef", bytearray(b"deadbeef"), 1, 8, 0, False, False, None),
        (b"\1deadbeef", bytearray(b"\0deadbeef"), 1, 8, 1, True, False, None),
        (b"\1deadbeef", bytearray(b"deadbeef"), 1, 8, 0, True, False, None),
        (b"\1deadbeef", b"\0deadbeef", 1, 8, 1, False, True, None),
        (b"\1deadbeef", b"deadbeef", 1, 8, 0, False, True, None),
        (b"\1deadbeef", b"\0deadbeef", 1, 8, 1, True, True, None),
        (b"\1deadbeef", b"deadbeef", 1, 8, 0, True, True, None),
        (b"lemenruss", bytearray(b"lemenruss"), None, 9, None, False, False, None),
        (b"\1backboneof", bytearray(b"backboneof"), 1, 10, None, False, False, None),
        (b"\1theguard", b"theguard", 1, 8, None, False, True, None),
    ],
)
def test_chunk_copy(
    src: bytes | bytearray,
    dest: bytes | bytearray,
    src_start: int | None,
    size: int | None,
    dest_start: int | None,
    src_is_stream: bool,
    dest_is_stream: bool,
    err: Type[RelicToolError],
):
    with opt_stream(src, src_is_stream) as copy_src:
        empty_dest = b"\0" * len(dest)
        empty_dest = (
            bytearray(empty_dest) if isinstance(dest, bytearray) else empty_dest
        )
        with opt_stream(empty_dest, dest_is_stream) as copy_dest:
            try:
                chunk_copy(copy_src, copy_dest, src_start, size, dest_start)
                if isinstance(copy_dest, BytesIO):
                    result = copy_dest.getvalue()
                else:
                    result = copy_dest
                assert result == dest

            except Exception as e:
                if not err:
                    raise
                else:
                    assert isinstance(e, err)
            else:
                if err:
                    pytest.fail("Expected an error")


@pytest.mark.parametrize(
    ["stream", "start", "size", "make_stream", "result"],
    [
        [b"BloodForTheBloodGod", 16, 3, False, b"God"],
        [b"BloodForTheBloodGod", None, 5, False, b"Blood"],
        [b"BloodForTheBloodGod", 5, None, False, b"ForTheBloodGod"],
        [b"BloodForTheBloodGod", None, None, False, b"BloodForTheBloodGod"],
        [b"BloodForTheBloodGod", 16, 3, True, b"God"],
        [b"BloodForTheBloodGod", None, 5, True, b"Blood"],
        [b"BloodForTheBloodGod", 5, None, True, b"ForTheBloodGod"],
        [b"BloodForTheBloodGod", None, None, True, b"BloodForTheBloodGod"],
        [bytearray(b"BloodForTheBloodGod"), 16, 3, True, b"God"],
        [bytearray(b"BloodForTheBloodGod"), None, 5, True, b"Blood"],
        [bytearray(b"BloodForTheBloodGod"), 5, None, True, b"ForTheBloodGod"],
        [bytearray(b"BloodForTheBloodGod"), None, None, True, b"BloodForTheBloodGod"],
        [b"BloodForTheBloodGod", None, 64, True, b"BloodForTheBloodGod"],
    ],
)
def test_read_chunks(
    stream: Any, start: int | None, size: int | None, make_stream: bool, result: bytes
):
    with opt_stream(stream, make_stream) as reader:
        with BytesIO() as writer:
            for chunk in read_chunks(reader, start, size):
                writer.write(chunk)
            buffer = writer.getvalue()
            assert buffer == result


@pytest.mark.parametrize("buffer", [b"bob\0lob\1law\2", b"blahblahblah"])
@pytest.mark.parametrize("start_pos", [0, 6, 12])
def test_tell_end(buffer: bytes, start_pos: int):
    with BytesIO(buffer) as stream:
        stream.seek(start_pos)
        expected_end = len(buffer)
        end = tell_end(stream)
        assert end == expected_end
        now = stream.tell()
        expected_now = start_pos
        assert now == expected_now


def _zcomp(b: bytes):
    return zlib.compress(b)


@pytest.mark.parametrize(
    "buffer",
    [
        b"LoremIpsum\0\1\2\3BobLobLaw\4\5\6\7ForTheEmperor\x08\x09\x0A\x0BDeathToTheEmporer\x0C\x0D\x0E\x0F"
    ],
)
class TestZlibFileReader:
    def test_init(self, buffer: bytes):
        with BytesIO(buffer) as stream:
            _ = ZLibFileReader(stream)

    def test_remaining(self, buffer: bytes):
        with BytesIO(_zcomp(buffer)) as stream:
            _ = ZLibFileReader(stream)
            now = len(buffer) // 2
            remaining = len(buffer) - now
            _._now = now  # cheat
            assert _._remaining == remaining

    def test_read(self, buffer: bytes):
        with BytesIO(_zcomp(buffer)) as stream:
            _ = ZLibFileReader(stream)
            read_size = len(buffer) // 2
            expected = buffer[:read_size]
            result = _.read(read_size)
            assert result == expected

    @pytest.mark.parametrize("when", [os.SEEK_SET, os.SEEK_CUR, os.SEEK_END, -1])
    def test_seek(self, buffer: bytes, when: int):
        with BytesIO(_zcomp(buffer)) as stream:
            _ = ZLibFileReader(stream)
            fake_now = _._now = len(buffer) // 2
            try:

                now = _.seek(0, when)
                if when == os.SEEK_SET:
                    assert now == 0
                elif when == os.SEEK_CUR:
                    assert now == fake_now
                elif when == os.SEEK_END:
                    assert _._remaining == 0
            except ValueError as e:
                if when not in [os.SEEK_SET, os.SEEK_CUR, os.SEEK_END]:
                    pass
                else:
                    raise e
            else:
                if when not in [os.SEEK_SET, os.SEEK_CUR, os.SEEK_END]:
                    pytest.fail("Expected failure because when was not a valid value")

    @pytest.mark.parametrize("when", [os.SEEK_SET, os.SEEK_CUR, os.SEEK_END])
    def test_tell(self, buffer: bytes, when: int):
        with BytesIO(_zcomp(buffer)) as stream:
            _ = ZLibFileReader(stream)
            fake_now = _._now = len(buffer) // 2
            _.seek(0, when)
            now = _.tell()
            if when == os.SEEK_SET:
                assert now == 0
            elif when == os.SEEK_CUR:
                assert now == fake_now
            elif when == os.SEEK_END:
                assert _._remaining == 0
            else:
                pytest.fail("Expected failure because when was not a valid value")

    def test_writeable(self, buffer: bytes):
        with BytesIO(_zcomp(buffer)) as stream:
            _ = ZLibFileReader(stream)
            writable = _.writable()
            assert writable is False
