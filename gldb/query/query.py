from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Any, Dict


class AbstractQuery(ABC):
    pass
    # def __init__(self, query: str,
    #              description: str = None,
    #              *args,
    #              **kwargs):
    #     self.query = query
    #     self.description = description
    #     self._args = args
    #     self._kwargs = kwargs


class QueryResult:

    def __init__(self, query: AbstractQuery, data: Any, description: str = None):
        self.query = query
        self.data = data
        self.description = description

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"{self.__class__.__name__}(\n  query={self.query},\n  data={self.data},\n  description={self.description}\n)"


@dataclass(frozen=True)
class FederatedQueryResult:
    data: Any
    metadata: Dict


class Query(AbstractQuery, ABC):

    def __call__(self, query, description=None, *args, **kwargs):
        return self.execute(query, description, *args, **kwargs)

    @abstractmethod
    def execute(self, query, description=None, *args, **kwargs) -> QueryResult:
        """Executes the query."""
