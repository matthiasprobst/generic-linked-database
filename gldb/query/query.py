from abc import ABC, abstractmethod


class Query(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Executes the query."""
