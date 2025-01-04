from abc import ABC, abstractmethod
from typing import Any


class AbstractQuery(ABC):

    @property
    @abstractmethod
    def description(self):
        """Returns a description of the query."""


class QueryResult:

    def __init__(self, query: AbstractQuery, result: Any):
        self.query = query
        self.result = result

    def __len__(self):
        return len(self.result)


class Query(AbstractQuery, ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> QueryResult:
        """Executes the query."""
