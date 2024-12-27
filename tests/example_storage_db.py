import pathlib

import pandas as pd

from gldb import StorageDatabase


class CSVDatabase(StorageDatabase):

    def __init__(self):
        self._filenames = []
        self.tables = {}

    def upload_file(self, filename):
        filename = pathlib.Path(filename)
        assert filename.exists(), f"File {filename} does not exist."
        if filename.resolve().absolute() in self._filenames:
            return
        self._filenames.append(filename.resolve().absolute())

        table_name = filename.name

        self.tables[table_name] = pd.read_csv(filename)

    def query(self, *args, **kwargs):
        return f"Querying data from {self}"

    def get_all(self, table_name):
        return self.tables[table_name]
