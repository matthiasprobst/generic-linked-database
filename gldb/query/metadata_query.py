from abc import ABC

import rdflib

from gldb.query.query import Query, QueryResult


class MetadataStoreQuery(Query, ABC):
    """RDF Store Query interface."""


class SparqlQuery(MetadataStoreQuery):

    def __repr__(self):
        return f"{self.__class__.__name__}({self.query!r})"

    def __str__(self):
        return self.query

    def execute(self, graph: rdflib.Graph) -> QueryResult:
        return QueryResult(
            query=self,
            data=graph.query(self.query, *self._args, **self._kwargs)
        )
