import unittest

from gldb.query import Query, QueryResult


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
