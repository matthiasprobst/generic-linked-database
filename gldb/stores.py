import pathlib
from abc import ABC, abstractmethod
from typing import Dict, Union, Any, Type

import rdflib

from gldb.query import Query
from gldb.query.metadata_query import SparqlQuery


class Store(ABC):
    """Store interface."""

    @property
    @abstractmethod
    def query(self) -> Type[Query]:
        """Returns the query class for the store."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> Any:
        """Uploads a file to the store."""

    def __repr__(self):
        """String representation of the Store."""
        return f"{self.__class__.__name__}()"


class DataStore(Store, ABC):
    """Data store interface (concrete implementations can be sql or non sql databases)."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]):
        """Insert data into the data store."""


class MetadataStore(Store, ABC):
    """Metadata database interface using."""

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> bool:
        """Insert data into the data store."""


class RDFStore(MetadataStore):
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
        """Return graph for the metadata store."""

    @property
    def query(self):
        return SparqlQuery(self.graph)


class StoreManager:
    """Store manager that manages the interaction between stores."""

    def __init__(self, stores: Dict[str, Store] = None):
        self._stores: Dict[str, DataStore] = stores if stores is not None else {}

    def __getattr__(self, item) -> Store:
        """Allows access to stores as attributes."""
        if item in self.stores:
            return self.stores[item]
        return super().__getattr__(item)

    def __len__(self):
        """Returns the number of stores managed."""
        return len(self.stores)

    def __repr__(self):
        """String representation of the DataStoreManager."""
        store_names = ", ".join(self.stores.keys())
        return f"{self.__class__.__name__}(stores=[{store_names}])"

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
        if store_name in self.stores:
            raise ValueError(f"DataStore with name {store_name} already exists.")
        self.stores[store_name] = store
