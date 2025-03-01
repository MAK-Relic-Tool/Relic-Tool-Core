"""
Tools for handling entrypoints via class-based registries
"""

from __future__ import annotations

from typing import (
    TypeVar,
    Protocol,
    Union,
    Dict,
    Optional,
    Iterable,
    MutableMapping,
)

from relic.core.errors import RelicToolError
from relic.core.typeshed import entry_points

_TKey = TypeVar("_TKey")  # pylint: disable=invalid-name
_TKey_contra = TypeVar(  # pylint: disable=invalid-name
    "_TKey_contra", contravariant=True
)
_TKey_co = TypeVar("_TKey_co", covariant=True)  # pylint: disable=invalid-name
_TValue = TypeVar("_TValue")  # pylint: disable=invalid-name
_TValue_contra = TypeVar(  # pylint: disable=invalid-name
    "_TValue_contra", contravariant=True
)
_TValue_co = TypeVar("_TValue_co", covariant=True)  # pylint: disable=invalid-name


class KeyFunc(Protocol[_TKey_contra]):  # pylint: disable=too-few-public-methods
    """
    A function which converts an object to a string representation for an entrypoint

    :param key: The key to convert to a string
    :type key: _TKey_Contra

    :rtype: str
    :returns: The string of teh object that will be used as an entrypoint

    """

    def __call__(self, key: _TKey_contra) -> str:
        raise NotImplementedError


class AutoKeyFunc(
    Protocol[_TKey_co, _TValue_contra]
):  # pylint: disable=too-few-public-methods
    """
    A function which converts an object to a list of key objects. At least one key should be returned.

    :param value: The value to convert to a sequence of keys
    :type value: _TValue_contra

    :rtype: Iterable[_TKey_co]
    :returns: A sequence of keys, with at least one key returned

    """

    def __call__(self, value: _TValue_contra) -> Iterable[_TKey_co]:
        raise NotImplementedError


class EntrypointRegistry(MutableMapping[Union[str, _TKey], _TValue]):
    """
    A helper class allowing
    """

    def __init__(
        self,
        entry_point_path: str,
        key_func: Optional[KeyFunc[_TKey]] = None,
        auto_key_func: Optional[AutoKeyFunc[_TKey, _TValue]] = None,
        autoload: bool = True,
    ):
        self._backing: Dict[str, _TValue] = {}
        self._ep_group = entry_point_path
        self._key_func = key_func
        self._auto_key_func = auto_key_func
        self._autoload = autoload

    def _run_autoload(self) -> None:
        if not self._autoload:
            return
        self.load_entrypoints()
        self._autoload = False

    def __setitem__(self, key: Union[str, _TKey], value: _TValue) -> None:
        self._run_autoload()
        true_key = self._key2str(key)
        self._backing[true_key] = value

    def __getitem__(self, item: Union[str, _TKey]) -> _TValue:
        self._run_autoload()
        true_key = self._key2str(item)
        return self._backing[true_key]

    def __delitem__(self, key: Union[str, _TKey]) -> None:
        self._run_autoload()
        true_key = self._key2str(key)
        del self._backing[true_key]

    def __len__(self) -> int:
        self._run_autoload()
        return len(self._backing)

    def __iter__(self) -> Iterable[str]:  # type:ignore
        # Expects Iterable[Union[str,_TKey]]; but Iterable[str] acts identically (albeit with a different type)

        self._run_autoload()
        return iter(self._backing)

    def __contains__(self, key: object) -> bool:
        self._run_autoload()
        true_key = self._key2str(key)  # type: ignore
        return true_key in self._backing

    def __repr__(self) -> str:
        self._run_autoload()
        return repr(self._backing)

    def _key2str(self, key: Union[_TKey, str]) -> str:
        if isinstance(key, str):
            return key
        if self._key_func is not None:
            return self._key_func(key)

        raise RelicToolError(
            f"Key '{key}' cannot be converted to an EntryPoint Key!"
            f" No key_func was specified on creation, and _TKey is not a string!"
        )

    def _val2keys(self, value: _TValue) -> Iterable[_TKey]:
        if self._auto_key_func is not None:
            return self._auto_key_func(value)
        raise RelicToolError(
            f"Value '{value}' cannot automatically resolve it's key! No auto_key_func was specified on creation!"
        )

    def load_entrypoints(self) -> None:
        """
        Load all entrypoints from the group specified in __init__
        """
        for ep in entry_points().select(group=self._ep_group):
            ep_name: str = ep.name
            ep_func: _TValue = ep.load()
            self._raw_register(ep_name, ep_func)

    def _raw_register(self, key: str, value: _TValue) -> None:
        self._backing[key] = value

    def register(self, key: _TKey, value: _TValue) -> None:
        """
        Add the key-value pair to the registry, the key will be converted using the key_func.

        :param key: The key to use in the registry
        :type key: _TKey

        :param value: The value to register, under the given key
        :type value: _TValue
        """
        self[key] = value

    def auto_register(self, value: _TValue) -> None:
        """
        Automatically add the value to the entrypoint registry,
            using keys automatically determined from the auto_key_func.

        :param value: The value to register
        :type value: _TValue
        """
        keys = self._val2keys(value)
        for key in keys:
            self.register(key, value)


__all__ = ["KeyFunc", "AutoKeyFunc", "EntrypointRegistry"]
