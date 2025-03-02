import subprocess
from argparse import ArgumentError

# Local testing requires running `pip install -e "."`
from contextlib import redirect_stdout, redirect_stderr
import io
from typing import Sequence

import pytest


class CommandTests:
    def test_run(self, args: Sequence[str], output: str, exit_code: int, stdout: bool):
        cmd = subprocess.run(args, capture_output=True, text=True)
        result = cmd.stdout if stdout else cmd.stderr
        status = cmd.returncode
        print(f"'{result}'")  # Visual Aid for Debugging
        assert status == exit_code
        assert output in result

    def test_run_with(
        self, args: Sequence[str], output: str, exit_code: int, stdout: bool
    ):
        from relic.core.cli import CLI

        with io.StringIO() as f:
            if stdout:
                with redirect_stdout(f):
                    status = CLI.run_with(*args)
            else:
                with redirect_stderr(f):
                    status = CLI.run_with(*args)
            f.seek(0)
            result = f.read()
            print(f"'{result}'")  # Visual Aid for Debugging
            assert output in result
            assert status == exit_code


class CommandExceptionTests:

    def test_run(self, args: Sequence[str], exception: Exception, exit_code: int):
        cmd = subprocess.run(args, capture_output=True, text=True)
        result = cmd.stdout if False else cmd.stderr
        status = cmd.returncode
        print(f"'{result}'")  # Visual Aid for Debugging
        assert status == exit_code
        assert str(exception) in result

    def test_run_with(self, args: Sequence[str], exception: Exception, exit_code: int):
        from relic.core.cli import CLI

        try:
            status = CLI.run_with(*args)
            assert status == exit_code
        except Exception as caught:
            if isinstance(exception, ArgumentError) and isinstance(
                caught, ArgumentError
            ):
                assert caught.argument_name == exception.argument_name
                assert caught.message == exception.message
            else:
                assert caught == exception


def _ArgumentError(name: str, message: str):
    _ = ArgumentError(None, message)
    _.argument_name = name
    return _


_HELP = ["relic", "-h"], """usage: relic [-h]""", 0, True
_NO_SUB_CMD = ["relic"], """usage: relic [-h]""", 1, True
_T = """relic: error: argument command: invalid choice: '{name}' (choose from )"""
_BAD_SUB_CMD = (
    ["relic", "Paul_Chambers"],
    _ArgumentError("command", "invalid choice: 'Paul_Chambers' (choose from )"),
    2,
)


_PRINT_TESTS = [_HELP, _NO_SUB_CMD]
_PRINT_TEST_IDS = [" ".join(str(__) for __ in _[0]) for _ in _PRINT_TESTS]
_EX_TESTS = [_BAD_SUB_CMD]
_EX_TEST_IDS = [" ".join(str(__) for __ in _[0]) for _ in _EX_TESTS]


@pytest.mark.parametrize(
    ["args", "output", "exit_code", "stdout"], _PRINT_TESTS, ids=_PRINT_TEST_IDS
)
class TestRelicCli(CommandTests): ...


@pytest.mark.parametrize(
    [
        "args",
        "exception",
        "exit_code",
    ],
    _EX_TESTS,
    ids=_EX_TEST_IDS,
)
class TestRelicCliExceptions(CommandExceptionTests): ...
