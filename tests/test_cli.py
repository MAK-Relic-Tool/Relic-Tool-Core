import subprocess

# Local testing requires running `pip install -e "."`
from contextlib import redirect_stdout, redirect_stderr
import io
from typing import Sequence

import pytest


class CommandTests:
    def test_run(self, args: Sequence[str], output: str, exit_code: int):
        _args = ["relic", *args]
        cmd = subprocess.run(_args, capture_output=True, text=True)
        result = cmd.stdout
        err = cmd.stderr
        status = cmd.returncode
        print("STDOUT:")
        print(f"'{result}'")  # Visual Aid for Debugging
        print()
        print("STDERR:")
        print(f"'{err}'")
        assert status == exit_code
        assert output in result

    def test_run_with(self, args: Sequence[str], output: str, exit_code: int):
        from relic.core.cli import CLI

        with io.StringIO() as f:
            with io.StringIO() as ferr:
                with redirect_stdout(f):
                    with redirect_stderr(ferr):
                        status = CLI.run_with(*args)

                        result = f.getvalue()
                        err = ferr.getvalue()
                        print("STDOUT:")
                        print(f"'{result}'")  # Visual Aid for Debugging
                        print()
                        print("STDERR:")
                        print(f"'{err}'")
                        assert status == exit_code
                        assert output in result


_HELP = ["-h"], """usage: relic [-h] {} ...""", 0

_TESTS = [_HELP]
_TEST_IDS = [" ".join(_[0]) for _ in _TESTS]


@pytest.mark.parametrize(["args", "output", "exit_code"], _TESTS, ids=_TEST_IDS)
class TestRelicCli(CommandTests): ...
