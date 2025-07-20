import unittest

import rdflib

from gldb.query import Query, QueryResult, SparqlQuery


class TestVersion(unittest.TestCase):

    def test_query(self):

        class SQLQuery(Query):

            def execute(self, *args, **kwargs) -> QueryResult:
                return QueryResult(self, "result")

        q = SQLQuery("SELECT * FROM Customers;", "Get all customers")
        self.assertEqual(q.query, "SELECT * FROM Customers;")
        self.assertEqual(q.description, "Get all customers")

        res = q.execute()
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
        self.assertEqual(res.data, graph.query("SELECT * WHERE { ?s ?p ?o }"))
