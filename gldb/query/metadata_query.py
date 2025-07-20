from abc import ABC

from gldb.query.query import Query, QueryResult


class MetadataStoreQuery(Query, ABC):
    """RDF Store Query interface."""


class SparqlQuery(MetadataStoreQuery):

    def __init__(self, graph):
        """
        Initialize a SPARQL query.

        :param graph: The RDF graph to query.
        """
        self.graph = graph

    def __repr__(self):
        return f"{self.__class__.__name__}(graph={self.graph})"

    def execute(self, query, description=None, *args, **kwargs):
        return QueryResult(
            query=self,
            data=self.graph.query(query, *args, **kwargs),
            description=description
        )
