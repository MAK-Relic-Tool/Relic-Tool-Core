from __future__ import annotations

from importlib.metadata import entry_points, EntryPoint
from typing import (
    TypeVar,
    Protocol,
    Union,
    Dict,
    Optional,
    Iterable,
    MutableMapping,
    List,
)

from relic.core.errors import RelicToolError

_TKey = TypeVar("_TKey")
_TKey_contra = TypeVar("_TKey_contra", contravariant=True)
_TKey_cov = TypeVar("_TKey_cov", covariant=True)
_TValue = TypeVar("_TValue")
_TValue_contra = TypeVar("_TValue_contra", contravariant=True)
_TValue_cov = TypeVar("_TValue_cov", covariant=True)


class KeyFunc(Protocol[_TKey_contra]):
    """
    A function which converts an object to a string representation for an entrypoint

    :param key: The key to convert to a string
    :type key: _TKey_Contra

    :rtype: str
    :returns: The string of teh object that will be used as an entrypoint

    """
    def __call__(self, key: _TKey_contra) -> str:
        raise NotImplementedError


class AutoKeyFunc(Protocol[_TKey_cov, _TValue_contra]):
    """
    A function which converts an object to a list of key objects. At least one key should be returned.

    :param value: The value to convert to a sequence of keys
    :type value: _TValue_contra

    :rtype: Iterable[_TKey_cov]
    :returns: A sequence of keys, with at least one key returned

    """
    def __call__(self, value: _TValue_contra) -> Iterable[_TKey_cov]:
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

    def __iter__(
        self,
    ) -> Iterable[
        str
    ]:  # type:ignore # Expects Iterable[Union[str,_TKey]]; but Iterable[str] acts identically (albeit with a different type)
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
            f"Key '{key}' cannot be converted to an EntryPoint Key! No key_func was specified on creation, and _TKey is not a string!"
        )

    def _val2keys(self, value: _TValue) -> Iterable[_TKey]:
        if self._auto_key_func is not None:
            return self._auto_key_func(value)
        raise RelicToolError(
            f"Value '{value}' cannot automatically resolve it's key! No auto_key_func was specified on creation!"
        )

    def load_entrypoints(self) -> None:
        all_entrypoints: Dict[str, List[EntryPoint]] = entry_points()
        group_entrypoints: List[EntryPoint] = all_entrypoints.get(self._ep_group, [])
        for ep in group_entrypoints:
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
        Automatically add the value to the entrypoint registry, using keys automatically determined from the auto_key_func.

        :param value: The value to register
        :type value: _TValue
        """
        keys = self._val2keys(value)
        for key in keys:
            self.register(key, value)
