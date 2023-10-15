import subprocess

# Local testing requires running `pip install -e "."`
from contextlib import redirect_stdout
import io
from typing import Sequence

import pytest


class CommandTests:
    def test_run(self, args: Sequence[str], output: str, exit_code: int):
        _args = ["relic", *args]
        cmd = subprocess.run(_args, capture_output=True, text=True)
        result = cmd.stdout
        status = cmd.returncode
        print(f"'{result}'")  # Visual Aid for Debugging
        assert output in result
        assert status == exit_code

    def test_run_with(self, args: Sequence[str], output: str, exit_code: int):
        from relic.core.cli import cli_root
        with io.StringIO() as f:
            with redirect_stdout(f):
                status = cli_root.run_with(*args)
            f.seek(0)
            result = f.read()
            print(f"'{result}'")  # Visual Aid for Debugging
            assert output in result
            assert status == exit_code

_HELP = ["-h"], """usage: relic [-h] {} ...""", 0

_TESTS = [_HELP]
_TEST_IDS = [' '.join(_[0]) for _ in _TESTS]


@pytest.mark.parametrize(["args", "output", "exit_code"], _TESTS, ids=_TEST_IDS)
class TestRelicCli(CommandTests):
    ...
