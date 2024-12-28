import pathlib
from abc import ABC, abstractmethod
from typing import Union

from .store import DataStore


class RawDataStore(DataStore, ABC):
    """Data store interface (concrete implementations can be sql or non sql databases)."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        """Insert data into the data store."""
        pass
