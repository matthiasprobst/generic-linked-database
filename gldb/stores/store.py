import pathlib
from abc import ABC, abstractmethod
from typing import Union


class Store(ABC):
    """Store interface."""

    @abstractmethod
    def execute_query(self, query: 'Query'):
        """Executes the query on the store."""

    @property
    @abstractmethod
    def expected_file_extensions(self):
        """Returns the expected file extensions for the uploader."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> bool:
        """Uploads a file to the store."""
