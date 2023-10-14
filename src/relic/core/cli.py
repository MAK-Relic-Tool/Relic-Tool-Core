from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from typing import Optional, TYPE_CHECKING, Protocol

import pkg_resources

if TYPE_CHECKING:
    class _SubParsersAction:
        def add_parser(self, name, *, prog: Optional = None, aliases: Optional = None, help: Optional = None,
                       **kwargs) -> ArgumentParser:
            ...


class CliEntrypoint(Protocol):
    def __call__(self, parent: _SubParsersAction, autoload: bool):
        raise NotImplementedError


class _CliPlugin:
    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def run(self, *args):
        ns = self.parser.parse_args(args)
        if not hasattr(ns, "cmd"):
            raise NotImplementedError("Command defined in argparse, but it's function was not specified.")
        cmd = ns.cmd
        result = cmd(ns)
        if result is None:  # Assume success
            result = 0
        sys.exit(result)


class CliPluginGroup(_CliPlugin):
    GROUP = None

    def __init__(self, parent: _SubParsersAction, autoload: bool = True, **kwargs):
        if TYPE_CHECKING:
            self.subparsers = None
        if self.GROUP is None:
            raise ValueError
        parser = self._create_parser(parent)
        super().__init__(parser)
        self.subparsers = self._create_subparser_group(parser)
        if autoload:
            self._load(autoload)

    def _create_parser(self, command_group: Optional[_SubParsersAction] = None) -> ArgumentParser:
        raise NotImplementedError

    def _create_subparser_group(self, parser: ArgumentParser) -> _SubParsersAction:
        return parser.add_subparsers()

    def _load(self, autoload: bool = False):
        for ep in pkg_resources.iter_entry_points(group=self.GROUP):
            ep_func: CliEntrypoint = ep.load()
            ep_func(parent=self.subparsers, autoload=autoload)


class CliPlugin(_CliPlugin):
    def __init__(self, parent: Optional[_SubParsersAction], **kwargs):
        parser = self._create_parser(parent)
        super().__init__(parser)
        if self.parser.get_default("cmd") is None:
            self.parser.set_defaults(cmd=self.command)

    def _create_parser(self, command_group: Optional[_SubParsersAction] = None) -> ArgumentParser:
        raise NotImplementedError

    def command(self, ns: Namespace) -> Optional[int]:
        raise NotImplementedError


class RelicCli(CliPluginGroup):
    GROUP = "relic.cli"

    def _create_parser(self, command_group: Optional[_SubParsersAction] = None) -> ArgumentParser:
        if command_group is None:
            return ArgumentParser("relic")
        else:
            return command_group.add_parser("relic")
