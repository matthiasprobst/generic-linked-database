import unittest
from typing import Type

from gldb.query import Query, QueryResult
from gldb.stores import DataStore
from gldb.stores import StoreManager


class MockSqlQuery(Query):

    def __init__(self, query: str, description: str = None):
        super().__init__(query, description)
        self.query = query

    def execute(self, *args, **kwargs) -> QueryResult:
        return QueryResult(self, "mock_result")


class CSVDatabase(DataStore):

    def __init__(self):
        self._filenames = []
        self.tables = {}
        self._expected_file_extensions = {".csv", }

    @property
    def query(self) -> Type[Query]:
        return MockSqlQuery

    def upload_file(self, filename) -> bool:
        return True

    def execute_query(self, query: Query):
        raise NotImplementedError("CSVDatabase does not support queries.")


class TestDataStore(unittest.TestCase):

    def test_DataStoreManager(self):
        manager = StoreManager()
        self.assertEqual(len(manager), 0)
        self.assertEqual(
            manager.__repr__(),
            "StoreManager(stores=[])"
        )

    def test_add_store(self):
        manager = StoreManager()
        store = CSVDatabase()
        self.assertEqual(
            len(manager.stores),
            0
        )
        self.assertEqual(store.__repr__(), "CSVDatabase()")
        manager.add_store("test_store", store)

        self.assertEqual(len(manager), 1)

        with self.assertRaises(AttributeError):
            manager.does_not_exist

    def test_query_store(self):
        store = CSVDatabase()
        query = store.query(query="SELECT * FROM test_table;")
        self.assertIsInstance(query, Query)
        self.assertIsInstance(query, MockSqlQuery)
        self.assertEqual(query.query, "SELECT * FROM test_table;")

        qres = query.execute()
        self.assertIsInstance(qres, QueryResult)
        self.assertEqual(qres.data, "mock_result")
