import unittest

import rdflib

from gldb.query import Query, QueryResult, SparqlQuery
from gldb.query.metadata_query import sparql_result_to_df


class TestQuery(unittest.TestCase):

    def test_query(self):
        class SQLQuery(Query):

            def execute(self, query, description=None, *args, **kwargs) -> QueryResult:
                return QueryResult(self, data="result", description=description)

        q = SQLQuery()
        res = q("SELECT * FROM Customers;", "Get all customers")
        self.assertEqual(res.query, q)
        self.assertEqual(res.description, "Get all customers")

        res = q.execute("SELECT * FROM Customers;", "Get all customers")
        self.assertIsInstance(res, QueryResult)

    def test_sparql_query(self):
        graph = rdflib.Graph()
        sparql_query = SparqlQuery(graph)
        self.assertEqual(
            sparql_query.__repr__(),
            f"SparqlQuery(graph={graph})"
        )

        res = sparql_query("SELECT * WHERE { ?s ?p ?o }")
        self.assertIsInstance(res, QueryResult)
        self.assertEqual(res.query, sparql_query)
        self.assertTrue(res.data.equals(sparql_result_to_df(graph.query("SELECT * WHERE { ?s ?p ?o }"))))
