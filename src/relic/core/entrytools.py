from importlib.metadata import EntryPoint
from collections import MutableMapping
from typing import TypeVar, Protocol, Union, Dict, Optional, Iterable

import pkg_resources

from relic.core.errors import RelicToolError

_TKey = TypeVar("_TKey")
_TValue = TypeVar("_TValue")

class KeyFunc(Protocol[_TKey]):
    def __call__(self, key:_TKey) -> str:
        raise NotImplementedError

class AutoKeyFunc(Protocol[_TValue]):
    def __call__(self, key:_TValue) -> Iterable[_TKey]:
        raise NotImplementedError

class EntrypointRegistry(MutableMapping[Union[_TKey,str],_TValue]):

    def __init__(self, entry_point_path: str, data:Optional[Dict[_TKey,_TValue]] = None, key_func:Optional[KeyFunc] = None, auto_key_func:Optional[AutoKeyFunc] = None, autoload:bool=True):
        self._backing = {}
        if data is not None:
            self._backing.update(data)
        self._ep_group = entry_point_path
        self._key_func = key_func
        self._auto_key_func = auto_key_func
        if autoload:
            self.load_entrypoints()
        self._autoload = autoload


    def __setitem__(self, key, value):
        true_key = self._key2str(key)
        self._backing[true_key] = value

    def __getitem__(self, item) -> _TValue:
        true_key = self._key2str(item)
        return self._backing[true_key]

    def __delitem__(self, key):
        true_key = self._key2str(key)
        del self._backing[true_key]

    def __len__(self):
        return len(self._backing)

    def __iter__(self):
        return iter(self._backing)

    def __contains__(self, key):
        return key in self._backing

    def __repr__(self):
        return repr(self._backing)

    def __or__(self, other):
        if isinstance(other, EntrypointRegistry):
            backing = self._backing | other._backing
        elif isinstance(other, dict):
            backing = self._backing | other
        else:
            raise NotImplementedError
        return self.__copy_with_newdata(backing)

    def __copy_with_newdata(self, new_data):
        return self.__class__(
            self._ep_group,
            new_data,
            self._key_func,
            self._auto_key_func,
            self._autoload
        )

    def __ror__(self, other):
        if isinstance(other, EntrypointRegistry):
            backing = other._backing | self._backing
        elif isinstance(other, dict):
            backing = other | self._backing
        else:
            return NotImplemented
        return self.__copy_with_newdata(backing)

    def __ior__(self, other):
        if isinstance(other, EntrypointRegistry):
            self._backing |= other._backing
        else:
            self._backing |= other
        return self

    def __copy__(self):
        return self.__copy_with_newdata(self._backing.copy())

    def copy(self):
        if self.__class__ is EntrypointRegistry:
            return self.__copy_with_newdata(self._backing.copy())
        else:
            raise NotImplementedError

    @classmethod
    def fromkeys(cls, iterable, value=None):
        raise NotImplementedError



    def _key2str(self, key:_TKey) -> str:
        if self._key_func is not None:
            return self._key_func(key)
        elif isinstance(key,str):
            return key
        else:
            raise RelicToolError(f"Key '{key}' cannot be converted to an EntryPoint Key! No key_func was specified on creation, and _TKey is not a string!")

    def _val2keys(self, value:_TValue) -> Iterable[_TKey]:
        if self._auto_key_func is not None:
            return self._auto_key_func(value)
        else:
            raise RelicToolError(f"Value '{value}' cannot automatically resolve it's key! No auto_key_func was specified on creation!")

    def load_entrypoints(self) -> None:
        for ep in pkg_resources.iter_entry_points(group=self._ep_group):
            ep:EntryPoint
            ep_name: str = ep.name
            ep_func: _TValue = ep.load()
            self._raw_register(ep_name,ep_func)

    def _raw_register(self, key:str,value:_TValue):
        self._backing[key] = value

    def register(self, key: _TKey, value: _TValue) -> None:
        self[key] = value

    def auto_register(self, value: _TValue) -> None:
        keys = self._val2keys(value)
        for key in keys:
            self.register(key, value)