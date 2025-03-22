import argparse
import logging
import os
import sys
from argparse import ArgumentParser, Namespace
from os.path import basename
from typing import Any, Optional, Type
from unittest.mock import patch

import pytest

from relic.core.cli import (
    _create_file_handler,
    apply_logging_handlers,
    CliPlugin,
    CliPluginGroup,
    RelicCli,
    _SubParsersAction,
    get_file_type_validator,
    get_dir_type_validator,
    get_path_validator,
    LoggingOptions,
    RelicArgParser,
)
from relic.core.errors import RelicArgParserError, UnboundCommandError
from tests.util import TempFileHandle

EXISTS_FILE_PATH = __file__
EXISTS_FOLD_PATH = os.path.join(__file__, "..")
INVALID_DIR_PATH = os.path.join(__file__, "doesnotexist.txt")
NONEXIST_PATH = os.path.join(__file__, "..\\doesnotexist.txt")


@pytest.mark.parametrize(
    "level",
    [
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ],
)
def test_create_file_handler(level: int):
    # TODO, better test than 'it doesn't error'
    with TempFileHandle() as h:
        handler = _create_file_handler(h.path, level)


@pytest.mark.parametrize("print_log", [True, False])
@pytest.mark.parametrize("specify_log_file", [True, False])
@pytest.mark.parametrize("specify_log_config", [True, False])
def test_setup_logging_for_cli(
    specify_log_config: bool, specify_log_file: bool, print_log: bool
):
    with TempFileHandle() as logfile:
        with TempFileHandle() as logconfig:
            if specify_log_config:
                with logconfig.open("w") as h:
                    h.write(
                        "\n".join(
                            [
                                "[loggers]",
                                "keys=root",
                                "[handlers]",
                                "keys=h0",
                                "[formatters]",
                                "keys=f0",
                                "[formatter_f0]"
                                "format=F1 %(asctime)s %(levelname)s %(message)s",
                                "[handler_h0]",
                                "class=StreamHandler",
                                "level=NOTSET",
                                "formatter=f0",
                                "args=(sys.stdout,)",
                                "[logger_root]",
                                "level=NOTSET",
                                "handlers=h0",
                            ]
                        )
                    )

                ...  # Generate Config
            opt = LoggingOptions(
                log_level=logging.DEBUG,
                log_config=None if not specify_log_config else logconfig.path,
                log_file=None if not specify_log_file else logfile.path,
            )
            apply_logging_handlers(opt, print_log)


class FakeCliPlugin(CliPlugin):
    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            return command_group.add_parser("fake")
        else:
            return RelicArgParser("fake")

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        print("yay")
        return None


class FakeCliPluginAltFunc(CliPlugin):
    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            parser = command_group.add_parser("fake")
        else:
            parser = RelicArgParser("fake")
        parser.set_defaults(function=FakeCliPlugin.command)
        return parser

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        print("no!")
        return -1


@pytest.mark.parametrize(
    "cli",
    [RelicCli, FakeCliPlugin, FakeCliPluginAltFunc],
)
@pytest.mark.parametrize("parent", [True, False])
def test_init_cli(cli: Type[CliPlugin | CliPluginGroup], parent: bool):
    parent_parser: Optional[Any] = None
    if parent:
        parent_parser = argparse.ArgumentParser().add_subparsers()

    cli(parent=parent_parser)


def test_init_cli_group_none():
    try:
        CliPluginGroup()
    except RelicArgParserError:
        pass
    else:
        pytest.fail(
            "CliPlugin should have raised RelicArgParserError due to GROUP being set to None"
        )


@pytest.mark.parametrize(
    ["exists", "path", "should_fail"],
    [
        (True, EXISTS_FILE_PATH, False),
        (False, EXISTS_FILE_PATH, False),
        (True, EXISTS_FOLD_PATH, False),
        (False, EXISTS_FOLD_PATH, False),
        (True, NONEXIST_PATH, True),
        (False, NONEXIST_PATH, False),
        (True, INVALID_DIR_PATH, True),
        (False, INVALID_DIR_PATH, True),
    ],
)
def test_get_path_validator(exists: bool, path: str, should_fail: bool):
    validator = get_path_validator(exists)
    try:
        validator(path)
    except argparse.ArgumentTypeError:
        if not should_fail:
            pytest.fail("Validator failed when it was expected to pass")
    else:
        if should_fail:
            pytest.fail("Validator passed when it was expected to fail")


@pytest.mark.parametrize(
    ["exists", "path", "should_fail"],
    [
        (True, EXISTS_FILE_PATH, True),
        (False, EXISTS_FILE_PATH, True),
        (True, EXISTS_FOLD_PATH, False),
        (False, EXISTS_FOLD_PATH, False),
        (True, NONEXIST_PATH, True),
        (False, NONEXIST_PATH, False),
        (True, INVALID_DIR_PATH, True),
        (False, INVALID_DIR_PATH, True),
    ],
)
def test_get_dir_type_validator(exists: bool, path: str, should_fail: bool):
    validator = get_dir_type_validator(exists)
    try:
        validator(path)
    except argparse.ArgumentTypeError:
        if not should_fail:
            pytest.fail("Validator failed when it was expected to pass")
    else:
        if should_fail:
            pytest.fail("Validator passed when it was expected to fail")


@pytest.mark.parametrize(
    ["exists", "path", "should_fail"],
    [
        (True, EXISTS_FILE_PATH, False),
        (False, EXISTS_FILE_PATH, False),
        (True, EXISTS_FOLD_PATH, True),
        (False, EXISTS_FOLD_PATH, True),
        (True, NONEXIST_PATH, True),
        (False, NONEXIST_PATH, False),
        (True, INVALID_DIR_PATH, True),
        (False, INVALID_DIR_PATH, True),
    ],
)
def test_get_file_type_validator(exists: bool, path: str, should_fail: bool):
    validator = get_file_type_validator(exists)
    try:
        validator(path)
    except argparse.ArgumentTypeError:
        if not should_fail:
            pytest.fail("Validator failed when it was expected to pass")
    else:
        if should_fail:
            pytest.fail("Validator passed when it was expected to fail")


dummy_cli = RelicCli()


class DummyCliPlugin(CliPlugin):
    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            return command_group.add_parser("dummy")
        else:
            return RelicArgParser("dummy")

    def command(self, ns: Namespace, *, logger: logging.Logger) -> int:
        logger.info("Dummy")
        return 0


class ManualSetFunctionCliPlugin(CliPluginGroup):
    GROUP = "relic.cli.manset"

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            parser = command_group.add_parser("manset")
        else:
            parser = RelicArgParser("manset")
        parser.set_defaults(
            function=self.command
        )  # More practical to replace with custom help or something
        return parser

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        logger.info("Manual")
        return None


class ForceArgErrorCliPlugin(CliPlugin):
    def __init__(self, parent: _SubParsersAction | None):
        super().__init__(parent)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            return command_group.add_parser("arg_err")
        else:
            return RelicArgParser("arg_err")

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        raise argparse.ArgumentError(None, "Forced Arg Error")


class ForceRelicParserErrorCliPlugin(CliPlugin):
    def __init__(self, parent: _SubParsersAction | None):
        super().__init__(parent)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is not None:
            return command_group.add_parser("parser_err")
        else:
            return RelicArgParser("parser_err")

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        raise RelicArgParserError("Forced Parser Error")


DummyCliPlugin(dummy_cli.subparsers)  # init dummy command
ForceArgErrorCliPlugin(dummy_cli.subparsers)
ForceRelicParserErrorCliPlugin(dummy_cli.subparsers)
ManualSetFunctionCliPlugin(dummy_cli.subparsers)


@pytest.mark.parametrize("cli", [dummy_cli])
@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["relic", "-h"], 0),
        (["relic", "manset"], 0),
        (["relic", "dummy"], 0),
        (["relic", "parser_err"], 2),
        (["relic", "arg_err"], 2),
    ],
)
def test_cli_run(cli: CliPlugin, args: list[str], expected: Optional[int]):
    with patch.object(sys, "argv", args):
        try:
            cli.run()
        except SystemExit as e:
            assert e.code == expected


@pytest.mark.parametrize("cli", [dummy_cli])
@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["relic", "-h"], 0),
        (["relic", "dummy"], 0),
        (["-h"], 0),
        (["dummy"], 0),
    ],
)
def test_cli_run_with(cli: CliPlugin, args: list[str], expected: Optional[int]):
    status = cli.run_with(*args)
    assert status == expected


@pytest.mark.parametrize("cli", [dummy_cli])
@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["relic", "parser_err"], RelicArgParserError),
        (["relic", "arg_err"], argparse.ArgumentError),
        (["parser_err"], RelicArgParserError),
        (["arg_err"], argparse.ArgumentError),
    ],
)
def test_cli_run_with_error(cli: CliPlugin, args: list[str], expected: Type[Exception]):
    try:
        _ = cli.run_with(*args)
    except expected:
        pass
    else:
        pytest.fail(f"Expected '{expected}' error")


@pytest.mark.parametrize("log_file", [True, False])
@pytest.mark.parametrize("log_config", [True, False])
@pytest.mark.parametrize("print_log", [True, False])
def test_apply_logging_handlers(log_file: bool, log_config: bool, print_log: bool):
    with TempFileHandle(".logfile", create=log_file) as log_file_h:
        with TempFileHandle(".logcfg", create=log_config) as log_cfg_h:
            if log_config:
                with log_cfg_h.open("w") as writer:
                    writer.write(
                        """[loggers]
keys=root

[handlers]
keys=h0

[formatters]
keys=f0

[handler_h0]
class=logging.StreamHandler
formatter=f0
args=()

[formatter_f0]
class=logging.Formatter
format=%(levelname)s:%(asctime)s - %(message)s

[logger_root]
level=DEBUG
handlers=h0"""
                    )
            options = LoggingOptions(
                log_file=log_file_h.path,
                log_level=logging.DEBUG,
                log_config=log_cfg_h.path,
            )
            logger = logging.getLogger()
            with apply_logging_handlers(options, print_log, logger):
                logger.debug("blah")


def test_cli_unbound_func():
    try:
        dummy_cli._run(Namespace(), [])
    except UnboundCommandError:
        pass
    else:
        pytest.fail("Expected Unbound Command Error")


def test_command_name_captured():
    try:
        dummy_cli._run(Namespace(), [])
    except UnboundCommandError as e:
        expected = basename(dummy_cli.parser.prog)
        assert e.args[0] == expected
    else:
        pytest.fail("Expected Unbound Command Error")


def test_error_raises_relic_arg_parser_error():
    cli = RelicCli()
    try:
        cli.parser.add_subparsers()
    except RelicArgParserError:
        pass
    else:
        pytest.fail("Expected Relic Parser Error")


def test_preload():
    cli = RelicCli(load_on_create=False)
    cli._preload()
    # We cant assert loading cause i made it private -_-


def test_default_plugin_group_command():
    cli = RelicCli()
    result = cli.run_with()
    assert result == 1
