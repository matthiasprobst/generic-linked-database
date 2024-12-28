from abc import ABC, abstractmethod

from gldb.stores import Store


class Query(ABC):

    @abstractmethod
    def execute(self, store: Store):
        """
        Executes the query on the given store.

        :param store: The database or RDF store to query.
        :return: Query results.
        """
        pass
