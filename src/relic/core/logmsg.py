"""
Objects to allow logging to handle different string formatters
Including:
- Old Style  (E.G. '%s', '%(message)s')
- Brace (E.G. '{0}', '{message}')
- Dollar (N.E.G.)
"""

import logging
from typing import Any
from string import Template

logger = logging.getLogger(__name__)


class FormattedMessage:  # pylint: disable=R0903
    """
    Base Class for lazily formatting messages for logging
    All formatting logic should be placed in __str__ to allow the logger to discard any unprinted string conversions
    """

    def __init__(self, fmt: str, *args: Any, **kwargs: Any):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs
        self._init_warn()

    def _init_warn(self) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError


class BraceMessage(FormattedMessage):  # pylint: disable=R0903
    """
    Object to allow logging to handle the Brace string formatter '{0}' & '{message}'
    """

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


class DollarMessage(FormattedMessage):  # pylint: disable=R0903
    """
    Object to allow logging to handle the Dollar string formatter
    """

    def _init_warn(self) -> None:
        if len(self.args) > 0:
            logger.warning(
                "%s was passed %d positional arguments, which will be ignored",
                self.__class__,
                len(self.args),
            )

    def __str__(self) -> str:
        return Template(self.fmt).substitute(**self.kwargs)


class PercentMessage(FormattedMessage):  # pylint: disable=R0903
    """
    Object to allow logging to handle the Percent formatter '%s' & '%(message)s'
    logging supports this by default; this class is provided for convenience
    """

    def _init_warn(self) -> None:
        if len(self.kwargs) > 0 and len(self.args) > 0:
            logger.warning(
                "%s was passed %d keyword arguments and %d positional arguments,"
                " only one can be specified. Defaulting to keyword arguments",
                self.__class__,
                len(self.args),
                len(self.kwargs),
            )

    def __str__(self) -> str:
        fmt_args = self.kwargs if len(self.kwargs) > 0 else self.args
        return self.fmt % fmt_args


__all__ = [
    "FormattedMessage",
    "BraceMessage",
    "DollarMessage",
    "PercentMessage",
]
