from abc import ABC

import pandas as pd
import rdflib

from gldb.query.query import Query, QueryResult


def parse_literal(literal):
    if isinstance(literal, rdflib.Literal):
        return literal.value
    if isinstance(literal, rdflib.URIRef):
        return str(literal)
    return literal


def sparql_result_to_df(bindings):
    return pd.DataFrame([{str(k): parse_literal(v) for k, v in binding.items()} for binding in bindings])


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
            data=sparql_result_to_df(self.graph.query(query, *args, **kwargs).bindings),
            description=description
        )


class RemoteSparqlQuery(MetadataStoreQuery):

    def __init__(self, wrapper):
        """
        Initialize a remote SPARQL query.

        :param wrapper: An instance of SPARQLWrapper configured for the remote SPARQL endpoint.
        """
        self.wrapper = wrapper

    def __repr__(self):
        return f"{self.__class__.__name__}(endpoint={self.wrapper.endpoint})"

    def execute(self, query, description=None, *args, **kwargs) -> QueryResult:
        try:
            from SPARQLWrapper import SPARQLWrapper, JSON
        except ImportError:
            raise ImportError("Please install SPARQLWrapper to use this class: pip install SPARQLWrapper")
        sparql = self.wrapper
        sparql.setQuery(query)

        results = sparql.query().convert()

        bindings = results["results"]["bindings"]

        return QueryResult(
            query=self,
            data=bindings,
            description=description
        )
