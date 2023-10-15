from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from typing import Optional, TYPE_CHECKING, Protocol, Any, Union

import pkg_resources


# Circumvent mypy/pylint shenanigans ~
class _SubParsersAction:  # pylint: disable= too-few-public-methods # typechecker only, ignore warnings
    def add_parser(  # pylint: disable=redefined-builtin, unused-argument # typechecker only, ignore warnings
        self,
        name: str,
        *,
        prog: Optional[str] = None,
        aliases: Optional[Any] = None,
        help: Optional[str] = None,
        **kwargs: Any,
    ) -> ArgumentParser:
        raise NotImplementedError


class CliEntrypoint(Protocol):  # pylint: disable= too-few-public-methods
    def __call__(self, parent: Optional[_SubParsersAction]) -> Optional[int]:
        raise NotImplementedError


class _CliPlugin:  # pylint: disable= too-few-public-methods
    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def _run(self, ns: Namespace) -> int:
        if not hasattr(ns, "cmd"):
            raise NotImplementedError(
                "Command defined in argparse, but it's function was not specified."
            )
        cmd = ns.cmd
        result: Optional[int] = cmd(ns)
        if result is None:  # Assume success
            result = 0
        return result

    def run_with(self, *args: Any) -> Union[str, int, None]:
        try:
            ns = self.parser.parse_args(args)
            return self._run(ns)
        except SystemExit as sys_exit:
            return sys_exit.code

    def run(self) -> None:
        ns = self.parser.parse_args()
        exit_code = self._run(ns)
        sys.exit(exit_code)


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
        self._load()

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def _create_subparser_group(self, parser: ArgumentParser) -> _SubParsersAction:
        return parser.add_subparsers()  # type: ignore

    def _load(self) -> None:
        for ep in pkg_resources.iter_entry_points(group=self.GROUP):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers)


class CliPlugin(_CliPlugin):  # pylint: disable= too-few-public-methods
    def __init__(self, parent: Optional[_SubParsersAction] = None):
        parser = self._create_parser(parent)
        super().__init__(parser)
        if self.parser.get_default("cmd") is None:
            self.parser.set_defaults(cmd=self.command)

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


cli_root = RelicCli()
