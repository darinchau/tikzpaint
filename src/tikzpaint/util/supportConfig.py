from __future__ import annotations

# This module exists purely to implement first class support for copy and displayable
from abc import ABC, abstractmethod as virtual

"""This exists purely to add support for copying displayables"""

class _Config(ABC):
    @virtual
    def __copy__(self) -> _Config:
        raise NotImplementedError

class _ISupportConfig(ABC):
    @property
    @virtual
    def options(self) -> _Config:
        raise NotImplementedError

    def _set_config(self, config: _Config) -> None:
        """Sets the option of the object"""
        self._config = config.__copy__()
    
    @virtual
    def __copy__(self):
        raise NotImplementedError
    