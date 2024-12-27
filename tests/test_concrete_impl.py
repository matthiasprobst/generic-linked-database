import json
import logging
import pathlib
import sys
from typing import List

import rdflib

from gldb import GenericLinkedDatabase
from gldb.federated_query_result import FederatedQueryResult

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
        self._metadata_db = InMemoryRDFDatabase()
        self._storage_db = CSVDatabase()

    def upload_file(self, filename):
        filename = pathlib.Path(filename)
        assert filename.exists(), f"File {filename} does not exist."
        if filename.suffix in (".ttl", ".rdf", ".jsonld"):
            logger.info(f"Uploading file {filename} to the RDF database...")
            return self.metadata_db.upload_file(filename)
        return self.storage_db.upload_file(filename)

    def info(self):
        return f"GenericLinkedDatabaseImpl(metadata_db={self.metadata_db}, storage_db={self.storage_db})"

    @property
    def metadata_db(self) -> InMemoryRDFDatabase:
        return self._metadata_db

    @property
    def storage_db(self) -> CSVDatabase:
        return self._storage_db

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
        results = self.sparql(sparql_query)

        result_data = [{str(k): parse_literal(v) for k, v in binding.items()} for binding in results.bindings]

        federated_query_results = []

        for res in result_data:
            filename = str(res["url"]).rsplit('/', 1)[-1]

            data = self.storage_db.get_all(filename)

            # query all metadata for the dataset:
            metadata_sparql = """
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>

            SELECT ?p ?o
            WHERE {{
              <{dataset}> ?p ?o .
            }}
            """.format(dataset=res["dataset"])
            metadata_result = self.sparql(metadata_sparql)
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
    db.upload_file(__this_dir__ / "data/data1.jsonld")
    res = db.sparql("SELECT * WHERE {?s ?p ?o}")
    assert len(res) == 8, f"Expected 8 triples, got {len(res)}"

    db.upload_file(__this_dir__ / "data/metadata.jsonld")

    db.upload_file(__this_dir__ / "data/random_data.csv")
    db.upload_file(__this_dir__ / "data/random_data.csv")
    db.upload_file(__this_dir__ / "data/temperature.csv")
    db.upload_file(__this_dir__ / "data/users.csv")

    data = db.get_temperature_data_by_date(date="2024-01-01")

    # data = db.plot_temperature_data_by_date(date="2024-01-01")

    result = db.metadata_db.select(data[0].metadata["dcat:distribution"], serialization_format="json-ld", indent=4)
    print(result)


def parse_literal(literal):
    if isinstance(literal, rdflib.Literal):
        return literal.value
    if isinstance(literal, rdflib.URIRef):
        return str(literal)
    return literal


if __name__ == "__main__":
    test_concrete_impl()
