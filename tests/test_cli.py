import subprocess

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
        assert output in result
        assert status == exit_code

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


_HELP = ["relic", "-h"], """usage: relic [-h] {} ...""", 0, True
_NO_SUB_CMD = ["relic"], """usage: relic [-h] {} ...""", 1, False
_T = """relic: error: argument command: invalid choice: '{name}' (choose from )"""
_BAD_SUB_CMD = ["relic", "Paul_Chambers"], _T.format(name="Paul_Chambers"), 2, False


_TESTS = [_HELP, _NO_SUB_CMD, _BAD_SUB_CMD]
_TEST_IDS = [" ".join(str(__) for __ in _[0]) for _ in _TESTS]


@pytest.mark.parametrize(
    ["args", "output", "exit_code", "stdout"], _TESTS, ids=_TEST_IDS
)
class TestRelicCli(CommandTests):
    ...
