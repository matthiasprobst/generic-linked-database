import json
import logging
import pathlib
import sys
from typing import List, Union

import rdflib

from gldb import GenericLinkedDatabase
from gldb.federated_query_result import FederatedQueryResult
from gldb.query.rdfstorequery import SparqlQuery
from gldb.stores import DataStoreManager, DataStore

logger = logging.getLogger("gldb")
logger.setLevel(logging.DEBUG)
for h in logger.handlers:
    h.setLevel(logging.DEBUG)

__this_dir__ = pathlib.Path(__file__).parent

sys.path.insert(0, str(__this_dir__))
from example_rdf_database import InMemoryRDFDatabase
from example_storage_db import CSVDatabase


class GenericLinkedDatabaseImpl(GenericLinkedDatabase):

    def __init__(self):
        _store_manager = DataStoreManager()
        _store_manager.add_store("rdf_database", InMemoryRDFDatabase())
        _store_manager.add_store("csv_database", CSVDatabase())
        self._store_manager = _store_manager

    @property
    def store_manager(self) -> DataStoreManager:
        return self._store_manager

    def __getitem__(self, store_name) -> DataStore:
        return self.store_manager[store_name]

    # @property
    # def datastore(self) -> CSVDatabase:
    #     return self._storage_db

    def linked_upload(self, filename: Union[str, pathlib.Path]):
        raise NotImplemented("linked_upload not implemented")

    def get_temperature_data_by_date(self, date: str) -> List[FederatedQueryResult]:
        """High-level abstraction for user to find temperature data.
        It is a federated query that combines metadata and data from the RDF and CSV databases."""
        sparql_query = """
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?dataset ?url
        WHERE {{
          ?dataset a dcat:Dataset .
          ?dataset dcterms:created "{date}" .
          ?dataset dcat:distribution ?distribution .
          ?distribution dcat:downloadURL ?url .
        }}
        """.format(date=date)
        results = self["rdf_database"].execute_query(SparqlQuery(sparql_query))

        result_data = [{str(k): parse_literal(v) for k, v in binding.items()} for binding in results.bindings]

        federated_query_results = []

        for res in result_data:
            filename = str(res["url"]).rsplit('/', 1)[-1]

            data = self["csv_database"].get_all(filename)

            # query all metadata for the dataset:
            metadata_sparql = """
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>

            SELECT ?p ?o
            WHERE {{
              <{dataset}> ?p ?o .
            }}
            """.format(dataset=res["dataset"])
            metadata_result = self["rdf_database"].execute_query(SparqlQuery(metadata_sparql))
            dataset_result_data = [{str(k): v for k, v in binding.items()} for binding in
                                   metadata_result.bindings]
            metadata = {d["p"]: d["o"] for d in dataset_result_data}
            context = {"dcterms": "http://purl.org/dc/terms/", "dcat": "http://www.w3.org/ns/dcat#",
                       "ex": "https://example.org/"}

            g = rdflib.Graph()
            for k, v in metadata.items():
                g.add((rdflib.URIRef(res["dataset"]), rdflib.URIRef(k), v))
            jsonld = g.serialize(format="json-ld", context=context)
            jsonld_dict = json.loads(jsonld)
            for k, v in jsonld_dict.items():
                if isinstance(v, dict):
                    if len(v) == 1 and "@id" in v:
                        jsonld_dict[k] = v["@id"]
            federated_query_results.append(FederatedQueryResult(data=data, metadata=jsonld_dict))
            # better convert metadata to json-ld string

        return federated_query_results

    # def plot_temperature_data_by_date(self, date: str):
    #     datasets = self.get_temperature_data_by_date(date)
    #     plt.figure()
    #     for dataset in datasets:
    #         print("metadata of the plot: \n", json.dumps(dataset.metadata, indent=4))
    #         dataset.data.plot(x='timestamp', y='temperature', label=f"date={date}", ax=plt.gca())
    #     plt.xlabel('Time')
    #     plt.ylabel('Temperature')
    #     plt.legend()
    #     plt.show()
    #     return datasets


def test_concrete_impl():
    db = GenericLinkedDatabaseImpl()

    rdf_database = db["rdf_database"]
    csv_database = db["csv_database"]

    rdf_database.upload_file(__this_dir__ / "data/data1.jsonld")
    res = rdf_database.execute_query(SparqlQuery("SELECT * WHERE {?s ?p ?o}"))
    assert len(res) == 8, f"Expected 8 triples, got {len(res)}"

    rdf_database.upload_file(__this_dir__ / "data/metadata.jsonld")

    csv_database.upload_file(__this_dir__ / "data/random_data.csv")
    csv_database.upload_file(__this_dir__ / "data/random_data.csv")
    csv_database.upload_file(__this_dir__ / "data/temperature.csv")
    csv_database.upload_file(__this_dir__ / "data/users.csv")

    data = db.get_temperature_data_by_date(date="2024-01-01")

    # data = db.plot_temperature_data_by_date(date="2024-01-01")

    result = db["rdf_database"].select(data[0].metadata["dcat:distribution"], serialization_format="json-ld", indent=4)
    print(result)


def parse_literal(literal):
    if isinstance(literal, rdflib.Literal):
        return literal.value
    if isinstance(literal, rdflib.URIRef):
        return str(literal)
    return literal


if __name__ == "__main__":
    test_concrete_impl()
