from abc import ABC

import rdflib

from gldb.query.query import Query


class RDFStoreQuery(Query, ABC):
    """RDF Store Query interface."""


class SparqlQuery(RDFStoreQuery):

    def __init__(self, sparql_query: str, description: str="", *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._description = description
        self.sparql_query = sparql_query

    @property
    def description(self):
        return self._description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.sparql_query!r})"

    def __str__(self):
        return self.sparql_query

    def execute(self, graph: rdflib.Graph) -> rdflib.query.Result:
        return graph.query(self.sparql_query, *self._args, **self._kwargs)
