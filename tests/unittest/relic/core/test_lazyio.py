import contextlib
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
    class FakeSerializer:
        def __init__(self, stream: BinaryIO):
            self._serializer = stream

    @classmethod
    @contextlib.contextmanager
    def get_serializer(cls, buffer: bytes) -> Any:
        with BytesIO(buffer) as stream:
            yield cls.FakeSerializer(stream)

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
                assert inst._serializer.getvalue() == buffer


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
