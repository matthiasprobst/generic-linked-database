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


def sparql_result_to_df(sparql_result):
    return pd.DataFrame([{str(k): parse_literal(v) for k, v in binding.items()} for binding in sparql_result.bindings])


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
            data=sparql_result_to_df(self.graph.query(query, *args, **kwargs)),
            description=description
        )
