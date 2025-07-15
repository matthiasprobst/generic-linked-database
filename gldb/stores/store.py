import pathlib
from abc import ABC, abstractmethod
from typing import Dict, Union, Any

from gldb.query import Query, QueryResult


class DataStore(ABC):
    """Store interface."""

    @abstractmethod
    def execute_query(self, query: Query) -> QueryResult:
        """Executes the query on the store."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> Any:
        """Uploads a file to the store."""


class DataStoreManager:
    """Store manager that manages the interaction between stores."""

    def __init__(self):
        self.stores: Dict[str, DataStore] = {}

    def add_store(self, store_name: str, store: DataStore):
        """Add a new store to the manager."""
        self.stores[store_name] = store

    def get_store(self, store_name: str) -> DataStore:
        """Retrieve a store from the manager."""
        return self.stores[store_name]

    def __getitem__(self, store_name: str) -> DataStore:
        """Retrieve a store from the manager."""
        return self.stores[store_name]

    def execute_query(self, store_name: str, query: Query) -> QueryResult:
        """Executes a query on a specific store."""
        store = self.get_store(store_name)
        if store:
            return store.execute_query(query)
        raise ValueError(f"Store {store_name} not found.")

    def upload_file(self, store_name: str, filename: str):
        """Uploads a file to a specific store."""
        store = self.get_store(store_name)
        if store:
            return store.upload_file(filename)
        raise ValueError(f"Store {store_name} not found.")
