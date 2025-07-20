import logging
from typing import Dict

from .stores import Store, StoreManager

logger = logging.getLogger("gldb")


class GenericLinkedDatabase:

    def __init__(
            self,
            stores: Dict[str, Store]
    ):
        self._store_manager = StoreManager()
        for store_name, store in stores.items():
            if not isinstance(store, Store):
                raise TypeError(f"Expected Store, got {type(store)}")
            logger.debug(f"Adding store {store_name} to the database.")
            self.stores.add_store(store_name, store)

    @property
    def stores(self) -> StoreManager:
        """Returns the store manager."""
        return self._store_manager

    @property
    def metadata_stores(self) -> StoreManager:
        return StoreManager(
            self.stores.metadata_stores
        )

    @property
    def data_stores(self) -> StoreManager:
        """Alias for stores property."""
        return StoreManager(
            self.stores.data_stores
        )

    # @abstractmethod
    # def linked_upload(self, filename: Union[str, pathlib.Path]):
    #     """Uploads the file to both stores and links them."""

    # def execute_query(self, store_name: str, query: Query) -> QueryResult:
    #     return self.store_manager.execute_query(store_name, query)
