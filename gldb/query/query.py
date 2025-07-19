from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Any, Dict


class AbstractQuery(ABC):

    def __init__(self, query: str,
                 description: str = None,
                 *args,
                 **kwargs):
        self.query = query
        self.description = description
        self._args = args
        self._kwargs = kwargs


class QueryResult:

    def __init__(self, query: AbstractQuery, data: Any):
        self.query = query
        self.data = data

    def __len__(self):
        return len(self.data)


@dataclass(frozen=True)
class FederatedQueryResult:
    data: Any
    metadata: Dict


class Query(AbstractQuery, ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> QueryResult:
        """Executes the query."""
