import pathlib
from abc import ABC, abstractmethod
from typing import Union


class DataStore(ABC):
    """Data store interface (concrete implementations can be sql or non sql databases)."""

    @abstractmethod
    def query(self, *args, **kwargs):
        """Retrieve data from the data store."""
        pass

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        """Insert data into the data store."""
        pass
