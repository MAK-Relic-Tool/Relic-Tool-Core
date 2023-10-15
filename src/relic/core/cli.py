from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from typing import Optional, TYPE_CHECKING, Protocol, Any

import pkg_resources

if TYPE_CHECKING:
    # Circumvent mypy/pylint shenanigans
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
            ...


class CliEntrypoint(Protocol):  # pylint: disable= too-few-public-methods
    def __call__(
        self, parent: Optional[_SubParsersAction], autoload: bool
    ) -> Optional[int]:
        raise NotImplementedError


class _CliPlugin:  # pylint: disable= too-few-public-methods
    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def _run(self, ns: Namespace) -> None:
        if not hasattr(ns, "cmd"):
            raise NotImplementedError(
                "Command defined in argparse, but it's function was not specified."
            )
        cmd = ns.cmd
        result = cmd(ns)
        if result is None:  # Assume success
            result = 0
        sys.exit(result)

    def run_with(self, *args: Any) -> None:
        ns = self.parser.parse_args(args)
        self._run(ns)

    def run(self) -> None:
        ns = self.parser.parse_args()
        self._run(ns)


class CliPluginGroup(_CliPlugin):  # pylint: disable= too-few-public-methods
    GROUP: str = None  # type: ignore

    def __init__(
        self,
        parent: Optional[_SubParsersAction] = None,
        autoload: bool = True,
        **kwargs: Any,
    ):
        if TYPE_CHECKING:
            self.subparsers = None
        if self.GROUP is None:
            raise ValueError
        parser = self._create_parser(parent)
        super().__init__(parser)
        self.subparsers = self._create_subparser_group(parser)
        if autoload:
            self._load(autoload)

    def _create_parser(
        self, command_group: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        raise NotImplementedError

    def _create_subparser_group(self, parser: ArgumentParser) -> _SubParsersAction:
        return parser.add_subparsers()  # type: ignore

    def _load(self, autoload: bool = False) -> None:
        for ep in pkg_resources.iter_entry_points(group=self.GROUP):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers, autoload=autoload)


class CliPlugin(_CliPlugin):  # pylint: disable= too-few-public-methods
    def __init__(self, parent: Optional[_SubParsersAction] = None, **kwargs: Any):
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
