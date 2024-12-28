from abc import ABC, abstractmethod


class Query(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Executes the query on the given store.

        :param store: The database or RDF store to query.
        :return: Query results.
        """
        pass
