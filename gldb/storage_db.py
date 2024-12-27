import pathlib
from abc import ABC, abstractmethod
from typing import Union


class StorageDatabase(ABC):
    """Relational or non-relational database interface."""

    @abstractmethod
    def query(self, *args, **kwargs):
        """Retrieve data from the data store."""
        pass

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        """Insert data into the data store."""
        pass
