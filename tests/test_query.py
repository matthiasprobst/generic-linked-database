import pathlib
import sys
import unittest

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

from gldb.query import Query, QueryResult, SparqlQuery, RemoteSparqlQuery
from gldb.query.metadata_query import sparql_result_to_df
from gldb.stores import InMemoryRDFStore, RemoteSparqlStore

__this_dir__ = pathlib.Path(__file__).parent.resolve()


class TestQuery(unittest.TestCase):

    def test_query(self):
        class SQLQuery(Query):

            def execute(self) -> QueryResult:
                return QueryResult(self, data="result", description=self.description)

        q = SQLQuery("SELECT * FROM Customers;", "Get all customers")
        res = q.execute()
        self.assertEqual(res.query, q)
        self.assertEqual(res.description, "Get all customers")

        res = SQLQuery("SELECT * FROM Customers;", "Get all customers").execute()
        self.assertIsInstance(res, QueryResult)

    def test_sparql_query(self):
        graph = rdflib.Graph()
        sparql_query = SparqlQuery(query="SELECT * WHERE { ?s ?p ?o }")
        self.assertEqual(
            sparql_query.__repr__(),
            'SparqlQuery(query="SELECT * WHERE { ?s ?p ?o }", description="")'
        )
        store = InMemoryRDFStore(data_dir=__this_dir__ / "testdata")
        res = SparqlQuery("SELECT * WHERE { ?s ?p ?o }").execute(store)
        self.assertIsInstance(res, QueryResult)
        self.assertEqual(res.query, sparql_query)
        self.assertTrue(res.data.equals(sparql_result_to_df(graph.query("SELECT * WHERE { ?s ?p ?o }"))))

    def test_wikidata_query(self):
        enpoint_url = "https://query.wikidata.org/sparql"
        sparql_wrapper = SPARQLWrapper(enpoint_url)
        sparql_wrapper.setReturnFormat(JSON)
        query_str = """
SELECT * WHERE {
  wd:Q131448345 ?property ?value.
  OPTIONAL { ?value rdfs:label ?valueLabel. }
}
ORDER BY ?propertyLabel
"""
        sparql_query = RemoteSparqlQuery(query_str)
        self.assertEqual(
            sparql_query.__repr__(),
            f"RemoteSparqlQuery(query=\"{query_str}\", description=\"\")"
        )
        remote_store = RemoteSparqlStore(endpoint_url=enpoint_url, return_format="json")

        if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
            self.skipTest("Skipping test on non-3.11 Python to avoid rate limiting")

            res = sparql_query.execute(remote_store)
            self.assertIsInstance(res, QueryResult)
            self.assertEqual(res.query, sparql_query)
            self.assertTrue(len(res.data["results"]["bindings"]) >= 972)

            sparql_query = RemoteSparqlQuery(query="DESCRIBE wd:Q131448345")
            remote_store = RemoteSparqlStore(endpoint_url=enpoint_url, return_format="json-ld")
            res = sparql_query.execute(remote_store)
            print(res.data.serialize("json-ld").serialize())
