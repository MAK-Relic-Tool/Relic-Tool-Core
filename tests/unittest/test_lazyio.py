from io import BytesIO
from typing import BinaryIO, Optional

import pytest

from relic.core.lazyio import BinaryWrapper, BinarySerializer, BinaryWindow


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
