import logging
import pathlib
import warnings
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

    def upload_file(self, filename: Union[str, pathlib.Path]):
        filename = pathlib.Path(filename)
        success = False
        if filename.suffix in self.rdfstore.expected_file_extensions:
            success = self.rdfstore.upload_file(filename)
        if filename.suffix in self.datastore.expected_file_extensions:
            success = self.datastore.upload_file(filename)
        if not success:
            warnings.warn(f"File type {filename.suffix} not supported.")
        return success

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
