"""
Core files for implementing a Command Line Interface using Entrypoints


"""

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from importlib.metadata import entry_points, EntryPoint
from os.path import basename
from typing import Optional, TYPE_CHECKING, Protocol, Any, Union, List, Dict, Sequence

from relic.core.errors import UnboundCommandError


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
        result: Optional[int] = func(ns)
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
        except SystemExit as sys_exit:
            return sys_exit.code

    def run(self) -> None:
        """
        Run the command line interface, using arguments from sys.argv, then terminates the process.

        :returns: Nothing; the process is terminated
        :rtype: None
        """
        ns = self.parser.parse_args()
        exit_code = self._run(ns, sys.argv)
        sys.exit(exit_code)


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
        return parser.add_subparsers(dest="command")  # type: ignore

    def load_plugins(self) -> None:
        """
        Load all entrypoints using the group specified by the class-variable GROUP
        """

        all_entry_points: Dict[str, List[EntryPoint]] = entry_points()  # type: ignore[assignment, unused-ignore]
        for ep in all_entry_points.get(self.GROUP, []):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers)

    def command(self, ns: Namespace) -> Optional[int]:
        self.parser.print_help(sys.stderr)
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
        super().__init__(parser)
        if self.parser.get_default("function") is None:
            self.parser.set_defaults(function=self.command)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def command(self, ns: Namespace) -> Optional[int]:
        """
        Run the command line program

        :param ns: The arguments passed in, wrapped in a namespace object
        :type ns: Namespace

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
            return ArgumentParser("relic")
        return command_group.add_parser("relic")


CLI = RelicCli(
    load_on_create=False
)  # The root command line doesn't load plugins until it is called; all child plugins autoload as normal

if __name__ == "__main__":
    CLI.run()
