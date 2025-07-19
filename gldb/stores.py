import pathlib
from abc import ABC, abstractmethod
from typing import Dict, Union, Any, Type

import rdflib

from gldb.query import Query, QueryResult
from gldb.query.rdfstorequery import SparqlQuery


class Store(ABC):
    """Store interface."""

    @property
    @abstractmethod
    def query(self)  -> Type[Query]:
        """Returns the query class for the store."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> Any:
        """Uploads a file to the store."""


class DataStore(Store, ABC):
    """Data store interface (concrete implementations can be sql or non sql databases)."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        """Insert data into the data store."""
        pass


class MetadataStore(Store, ABC):
    """Metadata database interface using."""

    namespaces = {
        "ex": "https://example.org/",
        "afn": "http://jena.apache.org/ARQ/function#",
        "agg": "http://jena.apache.org/ARQ/function/aggregate#",
        "apf": "http://jena.apache.org/ARQ/property#",
        "array": "http://www.w3.org/2005/xpath-functions/array",
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
        "fn": "http://www.w3.org/2005/xpath-functions",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "geoext": "http://rdf.useekm.com/ext#",
        "geof": "http://www.opengis.net/def/function/geosparql/",
        "gn": "http://www.geonames.org/ontology#",
        "graphdb": "http://www.ontotext.com/config/graphdb#",
        "list": "http://jena.apache.org/ARQ/list#",
        "local": "https://doi.org/10.5281/zenodo.14175299/",
        "m4i": "http://w3id.org/nfdi4ing/metadata4ing#",
        "map": "http://www.w3.org/2005/xpath-functions/map",
        "math": "http://www.w3.org/2005/xpath-functions/math",
        "ofn": "http://www.ontotext.com/sparql/functions/",
        "omgeo": "http://www.ontotext.com/owlim/geo#",
        "owl": "http://www.w3.org/2002/07/owl#",
        "path": "http://www.ontotext.com/path#",
        "prov": "http://www.w3.org/ns/prov#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "rep": "http://www.openrdf.org/config/repository#",
        "sail": "http://www.openrdf.org/config/sail#",
        "schema": "https://schema.org/",
        "spif": "http://spinrdf.org/spif#",
        "sr": "http://www.openrdf.org/config/repository/sail#",
        "ssno": "https://matthiasprobst.github.io/ssno#",
        "wgs": "http://www.w3.org/2003/01/geo/wgs84_pos#",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    }

    @property
    @abstractmethod
    def graph(self) -> rdflib.Graph:
        pass

    @property
    def query(self):
        return SparqlQuery

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> bool:
        """Insert data into the data store."""
        pass


class StoreManager:
    """Store manager that manages the interaction between stores."""

    def __init__(self):
        self._stores: Dict[str, DataStore] = {}

    def __getitem__(self, store_name: str) -> Store:
        """Retrieve a store from the manager."""
        return self.stores[store_name]

    def __len__(self):
        """Returns the number of stores managed."""
        return len(self.stores)

    def __repr__(self):
        """String representation of the DataStoreManager."""
        store_names = ", ".join(self.stores.keys())
        return f"DataStoreManager(stores=[{store_names}])"

    @property
    def stores(self) -> Dict[str, Store]:
        """Returns the stores managed by the manager."""
        return self._stores

    @property
    def data_stores(self) -> Dict[str, DataStore]:
        """Alias for stores property."""
        return {k: v for k, v in self.stores.items() if isinstance(v, DataStore)}

    @property
    def metadata_stores(self) -> Dict[str, MetadataStore]:
        """Alias for stores property."""
        return {k: v for k, v in self.stores.items() if isinstance(v, MetadataStore)}

    def add_store(self, store_name: str, store: Store):
        """Add a new store to the manager."""
        self.stores[store_name] = store

    def get_store(self, store_name: str) -> Store:
        """Retrieve a store from the manager."""
        return self.stores[store_name]

    # def execute_query(self, store_name: str, query: Query) -> QueryResult:
    #     """Executes a query on a specific store."""
    #     store = self.get_store(store_name)
    #     if store:
    #         return store.execute_query(query)
    #     raise ValueError(f"Store {store_name} not found.")

    def upload_file(self, store_name: str, filename: str):
        """Uploads a file to a specific store."""
        store = self.get_store(store_name)
        if store:
            return store.upload_file(filename)
        raise ValueError(f"Store {store_name} not found.")
