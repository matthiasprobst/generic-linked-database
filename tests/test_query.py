import unittest

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

from gldb.query import Query, QueryResult, SparqlQuery, RemoteSparqlQuery
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

    def test_dbpedia_query(self):
        ENDPOINT_URL = "https://query.wikidata.org/sparql"
        sparql = SPARQLWrapper(ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql_query = RemoteSparqlQuery(sparql)
        self.assertEqual(
            sparql_query.__repr__(),
            f"RemoteSparqlQuery(endpoint={ENDPOINT_URL})"
        )

        res = sparql_query(
            """
SELECT * WHERE {
  wd:Q131448345 ?property ?value.
  OPTIONAL { ?value rdfs:label ?valueLabel. }
}
ORDER BY ?propertyLabel
"""
        )
        self.assertIsInstance(res, QueryResult)
        self.assertEqual(res.query, sparql_query)
        self.assertTrue(len(res.data) >= 972)

        res = sparql_query(
            """
SELECT * WHERE {
  wd:Q131549102 ?property ?value.
  OPTIONAL { ?value rdfs:label ?valueLabel. }
}
ORDER BY ?propertyLabel
"""
        )
        print(res)
