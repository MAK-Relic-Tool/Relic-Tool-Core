from typing import Any, Optional

import pytest

from relic.core.errors import _print_mismatch, UnboundCommandError, MismatchError


def _get_mismatch_message(name: str, received: Optional[Any], expected: Optional[Any]):
    mode = 0
    mode |= 1 << 0 if received is not None else 0
    mode |= 1 << 1 if expected is not None else 0
    formats = {
        0: "Unexpected {name}!",
        1: "Unexpected {name}; got `{received}`!",
        2: "Unexpected {name}; expected `{expected}`!",
        3: "Unexpected {name}; got `{received}`, expected `{expected}`!",
    }
    format_str = formats[mode]
    return format_str.format(name=name, received=received, expected=expected)


@pytest.mark.parametrize("name", ["Fake Name", "Dummy Test"])
@pytest.mark.parametrize(
    ["received", "expected"],
    [
        (b"\0", b"\1"),
        (867, 5309),
        ("cake", "pie"),
        (True, False),
        (None, None),
        (2004, None),
        (None, "0920"),
    ],
)
class TestPrintMismatch:
    def test_print_mismatch(
        self, name: str, received: Optional[Any], expected: Optional[Any]
    ):
        expected_str = _get_mismatch_message(name, received, expected)
        result_str = _print_mismatch(name, received, expected)
        assert result_str == expected_str

    def test_mismatch_error(
        self, name: str, received: Optional[Any], expected: Optional[Any]
    ):
        expected_str = _get_mismatch_message(name, received, expected)
        err = MismatchError(name, received, expected)
        result_str = str(err)
        assert result_str == expected_str


@pytest.mark.parametrize("name", ["unboundcommand", "Dummy Test"])
def test_unbound_command_error(name: str):
    expected_message = f"The '{name}' command was defined, but not bound to a function."
    err = UnboundCommandError(name)
    result_msg = str(err)
    assert result_msg == expected_message
