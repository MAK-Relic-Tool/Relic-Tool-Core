"""
Core files for implementing a Command Line Interface using Entrypoints


"""
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from typing import Optional, TYPE_CHECKING, Protocol, Any, Union

import importlib.metadata

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

    def _run(self, ns: Namespace) -> int:
        """
        Run the command using args provided by namespace

        :param ns: The namespace containing the args the command was called with
        :type ns: Namespace

        :raises NotImplementedError: The command was defined, but was not bound to a function

        :returns: An integer representing the status code; 0 by default if the command does not return a status code
        :rtype: int
        """

        if hasattr(ns, "command"):
            cmd = ns.command
        else:
            cmd = self.parser.prog

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
        if len(args) > 0 and self.parser.prog == args[0]:
            args = args[1:]  # allow prog to be first command
        try:
            self._pre_parse()
            ns = self.parser.parse_args(args)
            return self._run(ns)
        except SystemExit as sys_exit:
            return sys_exit.code

    def run(self) -> None:
        """
        Run the command line interface, using arguments from sys.argv, then terminates the process.

        :returns: Nothing; the process is terminated
        :rtype: None
        """
        self._pre_parse()
        ns = self.parser.parse_args()
        exit_code = self._run(ns)
        sys.exit(exit_code)

    def _pre_parse(self):
        pass


class CliPluginGroup(_CliPlugin):  # pylint: disable= too-few-public-methods
    GROUP: str = None  # type: ignore

    def __init__(
        self,
        parent: Optional[_SubParsersAction] = None,
    ):
        if TYPE_CHECKING:
            self.subparsers = None
        if self.GROUP is None:
            raise ValueError
        parser = self._create_parser(parent)
        super().__init__(parser)
        self.subparsers = self._create_subparser_group(parser)
        self.__loaded = False

    def _pre_parse(self):
        if not self.__loaded:
            self._load()

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def _create_subparser_group(self, parser: ArgumentParser) -> _SubParsersAction:
        return parser.add_subparsers(dest="command")  # type: ignore

    def _load(self) -> None:
        for ep in importlib.metadata.entry_points(group=self.GROUP):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers)


class CliPlugin(_CliPlugin):  # pylint: disable= too-few-public-methods
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
        raise NotImplementedError


class RelicCli(CliPluginGroup):  # pylint: disable= too-few-public-methods
    GROUP = "relic.cli"

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        if command_group is None:
            return ArgumentParser("relic")
        return command_group.add_parser("relic")


CLI = RelicCli()

if __name__ == "__main__":
    CLI.run()
