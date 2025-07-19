import logging
import pathlib
from abc import abstractmethod
from typing import Union, Dict

from .query import Query, QueryResult
from .stores import Store, DataStore, StoreManager, MetadataStore

logger = logging.getLogger("gldb")


class GenericLinkedDatabase:

    def __init__(
            self,
            stores: Dict[str, Store]
    ):
        self._store_managers = StoreManager()
        for store_name, store in stores.items():
            if not isinstance(store, Store):
                raise TypeError(f"Expected Store, got {type(store)}")
            if store_name in self._store_managers.stores:
                raise ValueError(f"DataStore with name {store_name} already exists.")
            logger.debug(f"Adding store {store_name} to the database.")
            self._store_managers.add_store(store_name, v)

    @property
    @abstractmethod
    def store_manager(self) -> StoreManager:
        """Returns the store manager."""

    @property
    def data_stores(self) -> Dict[str, DataStore]:
        """Alias for stores property."""
        return {k: v for k, v in self.store_manager.data_stores.items() if isinstance(v, DataStore)}

    @property
    def metadata_stores(self) -> Dict[str, MetadataStore]:
        """Alias for stores property."""
        return {k: v for k, v in self.store_manager.metadata_stores.items() if isinstance(v, DataStore)}

    def __getitem__(self, store_name) -> Store:
        return self.store_manager[store_name]

    @abstractmethod
    def linked_upload(self, filename: Union[str, pathlib.Path]):
        """Uploads the file to both stores and links them."""

    def execute_query(self, store_name: str, query: Query) -> QueryResult:
        return self.store_manager.execute_query(store_name, query)
