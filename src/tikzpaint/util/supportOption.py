from __future__ import annotations

# This module exists purely to implement first class support for copy and displayable
from abc import ABC, abstractmethod as virtual


class Options(ABC):
    @virtual
    def __copy__(self) -> Options:
        raise NotImplementedError

class _Support_Option(ABC):
    @property
    @virtual
    def options(self) -> Options:
        raise NotImplementedError

    def _set_options(self, option: Options) -> None:
        """Sets the option of the object"""
        self._options = option.__copy__()
    
    @virtual
    def __copy__(self):
        raise NotImplementedError
    