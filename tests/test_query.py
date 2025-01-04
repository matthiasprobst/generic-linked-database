import unittest

from gldb.query import Query, QueryResult


class TestVersion(unittest.TestCase):

    def test_query(self):
        class SQLQuery(Query):
            def __init__(self, query: str, description: str):
                self.query = query
                self._description = description

            @property
            def description(self):
                return self._description

            def execute(self, *args, **kwargs) -> QueryResult:
                return QueryResult(self, "result")

        q = SQLQuery("SELECT * FROM Customers;", "Get all customers")
        assert q.query == "SELECT * FROM Customers;"
        assert q.description == "Get all customers"

        res = q.execute()
        assert isinstance(res, QueryResult)
