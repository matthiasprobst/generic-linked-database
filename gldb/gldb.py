import logging
import pathlib
from abc import ABC, abstractmethod
from typing import Union

from .query import Query
from .stores import DataStore
from .stores import DataStoreManager

logger = logging.getLogger("gldb")


class GenericLinkedDatabase(ABC):

    @property
    @abstractmethod
    def store_manager(self) -> DataStoreManager:
        """Returns the store manager."""

    def __getitem__(self, store_name) -> DataStore:
        return self.store_manager[store_name]

    @abstractmethod
    def linked_upload(self, filename: Union[str, pathlib.Path]):
        """Uploads the file to both stores and links them."""

    def execute_query(self, store_name: str, query: Query):
        return self.store_manager.execute_query(store_name, query)
