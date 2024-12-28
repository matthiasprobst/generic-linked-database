import logging
import pathlib
from abc import ABC, abstractmethod
from typing import Union

from gldb.stores.datastore import DataStore
from gldb.stores.metadatastore import RDFStore
from .query import Query
from .query.datastorequery import DataStoreQuery
from .query.rdfstorequery import RDFStoreQuery

logger = logging.getLogger("gldb")


class GenericLinkedDatabase(ABC):

    @property
    @abstractmethod
    def rdfstore(self) -> RDFStore:
        """Returns the RDF Database (e.g. GraphDB)."""

    @property
    @abstractmethod
    def datastore(self) -> DataStore:
        """Returns the core database which can be relational (e.g. MySQL) or non-relational (e.g. MongoDB)."""

    @abstractmethod
    def linked_upload(self, filename: Union[str, pathlib.Path]):
        """Uploads the file to both stores and links them."""

    def execute_query(self, query: Query):
        if isinstance(query, RDFStoreQuery):
            return self.rdfstore.execute_query(query)
        elif isinstance(query, DataStoreQuery):
            return self.datastore.execute_query(query)
        else:
            raise ValueError(f"Query type {type(query)} not supported.")

    def sparql(self, sparql_query: str):
        logger.debug("Performing sparql query...")
        return self.rdfstore.graph.query(sparql_query)
