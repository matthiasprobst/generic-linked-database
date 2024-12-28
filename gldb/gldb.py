import logging
import pathlib
from abc import ABC, abstractmethod
from typing import Union

from .metadatastore import RDFStore
from .datastore import DataStore

logger = logging.getLogger("gldb")


class GenericLinkedDatabase(ABC):

    @property
    @abstractmethod
    def metadata_db(self) -> RDFStore:
        """Returns the RDF Database (e.g. GraphDB)."""

    @property
    @abstractmethod
    def storage_db(self) -> DataStore:
        """Returns the core database which can be relational (e.g. MySQL) or non-relational (e.g. MongoDB)."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        pass

    @abstractmethod
    def info(self):
        """Prints information about the database."""

    def sparql(self, sparql_query: str):
        logger.debug("Performing sparql query...")
        return self.metadata_db.graph.query(sparql_query)
