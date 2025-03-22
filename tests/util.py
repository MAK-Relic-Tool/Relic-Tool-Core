import contextlib
import os
import tempfile
from typing import Optional


class TempFileHandle:
    def __init__(self, suffix: Optional[str] = None, *, create: bool = True):
        if create:
            with tempfile.NamedTemporaryFile("x", delete=False, suffix=suffix) as h:
                self._filename = h.name
        else:
            self._filename = None

    @property
    def path(self):
        return self._filename

    def open(self, mode: str):
        return open(self._filename, mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._filename is not None:
                os.unlink(self._filename)
        except Exception as e:
            print(e)
