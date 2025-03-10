"""
Core files for implementing a Command Line Interface using Entrypoints
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from argparse import ArgumentParser, Namespace, ArgumentError
from dataclasses import dataclass
from gettext import gettext
from logging.config import fileConfig
from logging.handlers import RotatingFileHandler
from os.path import basename
from typing import (
    Optional,
    TYPE_CHECKING,
    Protocol,
    Any,
    Union,
    Sequence,
    Callable,
    Tuple,
)

from relic.core.errors import UnboundCommandError, RelicArgParserError, RelicArgParser
from relic.core.typeshed import entry_points

LOGLEVEL_TABLE = {
    "none": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def _arg_exists_err(value: str) -> argparse.ArgumentTypeError:
    return argparse.ArgumentTypeError(f"The given path '{value}' does not exist!")


def _get_path_validator(exists: bool) -> Callable[[str], str]:
    def _path_type(path: str) -> str:
        path = os.path.abspath(path)

        def _step(_path: str) -> None:
            parent, _ = os.path.split(_path)

            if len(parent) != 0 and parent != _path:
                return _step(parent)

            if not os.path.exists(parent):
                return None

            if os.path.isfile(parent):
                raise argparse.ArgumentTypeError(
                    f"The given path '{path}' is not a valid path; it treats a file ({parent}) as a directory!"
                )

            return None

        if exists and not os.path.exists(path):
            raise _arg_exists_err(path)

        _step(path)  # we want step to validate; but we dont care about its result

        return path

    return _path_type


def _get_dir_type_validator(exists: bool) -> Callable[[str], str]:
    validate_path = _get_path_validator(False)

    def _dir_type(path: str) -> str:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            if exists:
                raise _arg_exists_err(path)
            return validate_path(path)

        if os.path.isdir(path):
            return path

        raise argparse.ArgumentTypeError(f"The given path '{path}' is not a directory!")

    return _dir_type


def _get_file_type_validator(exists: Optional[bool]) -> Callable[[str], str]:
    validate_path = _get_path_validator(False)

    def _file_type(path: str) -> str:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            if exists:
                raise _arg_exists_err(path)
            return validate_path(path)

        if os.path.isfile(path):
            return path

        raise argparse.ArgumentTypeError(f"The given path '{path}' is not a file!")

    return _file_type


@dataclass
class LogingOptions:
    log_file: Optional[str]
    log_level: int
    log_config: Optional[str]


def _add_logging_to_parser(
    parser: ArgumentParser,
) -> None:
    """Adds [-l --log] and [-ll --loglevel] commands."""
    parser.add_argument(
        "--log",
        type=_get_file_type_validator(False),
        help="Path to the log file, if one is generated",
        nargs="?",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--loglevel",
        help="Verbosity of the log. Defaults to `info`",
        nargs="?",
        required=False,
        default="info",
        choices=list(LOGLEVEL_TABLE.keys()),
    )
    parser.add_argument(
        "--logconfig",
        type=_get_file_type_validator(True),
        help="Path to a logging config file.",
        nargs="?",
        required=False,
    )


def create_logger_from_namespace(ns: Namespace) -> logging.Logger:
    logger = logging.getLogger()
    options = _extract_logging_from_namespace(ns)
    setup_logging_for_cli(options, logger=logger)
    return logger


def _extract_logging_from_namespace(ns: Namespace) -> LogingOptions:
    log_file: Optional[str] = ns.log
    log_level_name: str = ns.loglevel
    log_level = LOGLEVEL_TABLE[log_level_name]
    log_config: Optional[str] = ns.logconfig
    return LogingOptions(log_file, log_level, log_config)


def _create_log_formatter() -> logging.Formatter:
    return logging.Formatter(
        fmt="%(levelname)s:%(name)s::%(filename)s:L%(lineno)d:\t%(message)s (%(asctime)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _create_file_handler(log_file: str, log_level: int) -> logging.FileHandler:
    f = _create_log_formatter()
    h = RotatingFileHandler(
        log_file,
        encoding="utf8",
        maxBytes=100000,
        backupCount=-1,
    )
    h.setFormatter(f)
    h.setLevel(log_level)
    return h


def _create_console_handlers(
    log_level: int, err_level: int = logging.WARNING
) -> Tuple[logging.Handler, logging.Handler]:
    f_out = logging.Formatter("%(message)s")
    f_err = _create_log_formatter()

    h_out = logging.StreamHandler(sys.stdout)
    h_err = logging.StreamHandler(sys.stderr)

    h_out.setFormatter(f_out)
    h_err.setFormatter(f_err)

    h_out.addFilter(lambda record: record.levelno < err_level)
    h_err.addFilter(lambda record: record.levelno >= err_level)

    h_out.setLevel(log_level)
    h_err.setLevel(max(err_level, log_level))
    return h_out, h_err


def setup_logging_for_cli(
    options: LogingOptions,
    print_log: bool = True,
    logger: Optional[logging.Logger] = None,
) -> None:
    logger = logger or logging.getLogger()  # Root logger
    # Run first to override other loggers
    if options.log_config is not None:
        fileConfig(options.log_config)

    logger.setLevel(options.log_level)

    if options.log_file is not None:
        h_log_file = _create_file_handler(options.log_file, options.log_level)
        logger.addHandler(h_log_file)

    if print_log:
        h_out, h_err = _create_console_handlers(options.log_level, logging.WARNING)
        logger.addHandler(h_out)
        logger.addHandler(h_err)


def _print_error(parser: ArgumentParser, message: str) -> None:
    parser.print_usage(sys.stderr)
    args = {"prog": parser.prog, "message": message}
    parser.exit(2, gettext("%(prog)s: error: %(message)s\n") % args)


# Circumvent mypy/pylint shenanigans ~
class _SubParsersAction:  # pylint: disable= too-few-public-methods # typechecker only, ignore warnings
    """
    A Faux class to fool MyPy because argparser does python magic to bind subparsers to their parent parsers
    """

    def add_parser(  # pylint: disable=redefined-builtin, unused-argument # typechecker only, ignore warnings
        self,
        name: str,
        *,
        prog: Optional[str] = None,
        aliases: Optional[Any] = None,
        help: Optional[str] = None,
        **kwargs: Any,
    ) -> ArgumentParser:
        """
        Adds a parser to the parent parser this is binded to.
        See argparse for more details.
        """
        raise NotImplementedError


class CliEntrypoint(Protocol):  # pylint: disable= too-few-public-methods
    """
    A protocol defining the expected entrypoint format when defining CLI Plugins

    """

    def __call__(self, parent: Optional[_SubParsersAction]) -> None:
        """
        Attach a parser to the parent subparser group.
        :param parent: The parent subparser group, if None, this is not being loaded as an entrypoint
        :type parent: Optional[_SubParsersAction]

        :returns: Nothing, if something is returned it should be ignored
        :rtype: None
        """
        raise NotImplementedError


class _CliPlugin:  # pylint: disable= too-few-public-methods
    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def _run(self, ns: Namespace, argv: Optional[Sequence[str]] = None) -> int:
        """
        Run the command using args provided by namespace

        :param ns: The namespace containing the args the command was called with
        :type ns: Namespace

        :param argv: The calling cli args; used only for error messages.
        :type argv: Optional[Sequence[str]], optional

        :raises UnboundCommandError: The command was defined, but was not bound to a function

        :returns: An integer representing the status code; 0 by default if the command does not return a status code
        :rtype: int
        """
        cmd = None
        if hasattr(ns, "command"):
            cmd = ns.command
            # if cmd is specified but not None; then argv[-1] may not be a command name
            if cmd is None and argv is not None and len(argv) > 0:
                cmd = argv[-1]  # get last part of command
        if cmd is None:
            cmd = basename(
                self.parser.prog
            )  # linux will list the full path of the command

        if not hasattr(ns, "function"):
            raise UnboundCommandError(cmd)
        func = ns.function
        logger = create_logger_from_namespace(ns)
        result: Optional[int] = func(ns, logger=logger)
        if result is None:  # Assume success
            result = 0
        return result

    def run_with(self, *args: str) -> Union[str, int, None]:
        """
        Run the command line interface with the given arguments.
        :param args: The arguments that will be run on the command line interface.
        :type args: str

        :returns: The status code or status message.
        :rtype: Union[str,int,None]
        """
        argv = args
        if len(args) > 0 and self.parser.prog == args[0]:
            args = args[1:]  # allow prog to be first command
        try:
            ns = self.parser.parse_args(args)
            return self._run(ns, argv)
        except SystemExit as sys_exit:  # Do not capture the exit
            return sys_exit.code

    def run(self) -> None:
        """
        Run the command line interface, using arguments from sys.argv, then terminates the process.

        :returns: Nothing; the process is terminated
        :rtype: None
        """
        try:
            ns = self.parser.parse_args()
            exit_code = self._run(ns, sys.argv)
            sys.exit(exit_code)
        except RelicArgParserError as e:
            _print_error(self.parser, e.args[0])
        except ArgumentError as e:
            _print_error(self.parser, str(e))


class CliPluginGroup(_CliPlugin):  # pylint: disable= too-few-public-methods
    """
    Create a Command Line Plugin which creates a command group which can autoload child plugins.

    :param parent: The parent parser group, that this command line will attach to.
        If None, the command line is treated as the root command line.
    :type parent: Optional[_SubParsersAction], optional

    :param load_on_create: Whether further plugins are loaded on creation, by default, this is True.
    :type load_on_create: bool, optional

    :note: The class exposes a class variable 'GROUP', which is used to automatically load child plugins.
    """

    GROUP: str = None  # type: ignore

    def __init__(
        self,
        parent: Optional[_SubParsersAction] = None,
        load_on_create: bool = True,
    ):
        if TYPE_CHECKING:
            self.subparsers = None
        if self.GROUP is None:
            raise ValueError
        parser = self._create_parser(parent)
        _add_logging_to_parser(parser)
        super().__init__(parser)
        self.subparsers = self._create_subparser_group(parser)
        if load_on_create:
            self.load_plugins()
        self.__loaded = load_on_create
        if self.parser.get_default("function") is None:
            self.parser.set_defaults(function=self.command)

    def _preload(self) -> None:
        if self.__loaded:
            return
        self.load_plugins()
        self.__loaded = True

    def run(self) -> None:
        self._preload()
        return super().run()

    def run_with(self, *args: str) -> Union[str, int, None]:
        self._preload()
        return super().run_with(*args)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def _create_subparser_group(self, parser: ArgumentParser) -> _SubParsersAction:
        return parser.add_subparsers(dest="command", parser_class=RelicArgParser)  # type: ignore

    def load_plugins(self) -> None:
        """
        Load all entrypoints using the group specified by the class-variable GROUP
        """

        for ep in entry_points().select(group=self.GROUP):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers)

    def command(
        self, ns: Namespace, *, logger: logging.Logger  # pylint: disable=W0613
    ) -> Optional[int]:
        """
        Adapter which extracts parsed CLI arguments from the namespace and runs the appropriate CLI command
        """
        logger.info(self.parser.format_help())
        return 1


class CliPlugin(_CliPlugin):  # pylint: disable= too-few-public-methods
    """
    Create a Command Line Plugin, which can be autoloaded by a plugin group.

    :param parent: The parent parser group, that this command line will attach to.
        If None, the command line is treated as the root command line.
        By default, None
    :type parent: Optional[_SubParsersActions]
    """

    def __init__(self, parent: Optional[_SubParsersAction] = None):
        parser = self._create_parser(parent)
        _add_logging_to_parser(parser)
        super().__init__(parser)
        if self.parser.get_default("function") is None:
            self.parser.set_defaults(function=self.command)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def command(self, ns: Namespace, *, logger: logging.Logger) -> Optional[int]:
        """
        Run the command line program

        :param ns: The arguments passed in, wrapped in a namespace object
        :type ns: Namespace

        :param logger: The logger object to print messages to
        :type logger: logging.Logger

        :returns: The exit status code, None implies a status code of 0
        :rtype: Optional[int]
        """
        raise NotImplementedError


class RelicCli(CliPluginGroup):  # pylint: disable= too-few-public-methods
    """
    Creates the root command line interface for the Relic-Tool

    :note: Can be run internally from the library via the run_with function.
    :note: To add a plugin to the tool; add an entrypoint under the 'relic.cli' group.
    """

    GROUP = "relic.cli"

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is None:
            return RelicArgParser("relic")
        return command_group.add_parser("relic")


CLI = RelicCli(
    load_on_create=False
)  # The root command line doesn't load plugins until it is called; all child plugins autoload as normal

if __name__ == "__main__":
    CLI.run()

__all__ = [
    "RelicArgParserError",  # Should move to relic.core.errors in next major
    "RelicArgParser",  # Should move to relic.core.errors in next major
    "CLI",
    "CliPlugin",
    "CliPluginGroup",
    "CliEntrypoint",
    "RelicCli",
]
