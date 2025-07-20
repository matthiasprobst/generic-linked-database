import pathlib
import shutil
from abc import ABC, abstractmethod
from typing import Dict, Union, Any, Type

import rdflib

from gldb.query import Query
from gldb.query.metadata_query import SparqlQuery, RemoteSparqlQuery


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


class RDFStore(MetadataStore, ABC):
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


class RemoteSparqlStore(MetadataStore):

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint

    @property
    def query(self) -> RemoteSparqlQuery:
        """Return graph for the DbPedia metadata store."""
        try:
            from SPARQLWrapper import SPARQLWrapper, JSON
        except ImportError:
            raise ImportError("Please install SPARQLWrapper to use this class: pip install SPARQLWrapper")
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setReturnFormat(JSON)
        return RemoteSparqlQuery(sparql)

    def upload_file(self, filename: Union[str, pathlib.Path]) -> bool:
        """Uploads a file to the remote SPARQL endpoint."""
        raise NotImplementedError("Remote SPARQL Store does not support file uploads.")


class StoreManager:
    """Store manager that manages the interaction between stores."""

    def __init__(self, stores: Dict[str, Store] = None):
        self._stores: Dict[str, DataStore] = stores if stores is not None else {}

    def __getattr__(self, item) -> Store:
        """Allows access to stores as attributes."""
        if item in self.stores:
            return self.stores[item]
        return super().__getattribute__(item)

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


# concrete implementations of Store

class InMemoryRDFStore(RDFStore):
    """In-memory RDF database that can upload files and return a combined graph."""

    _expected_file_extensions = {".ttl", ".rdf", ".jsonld"}

    def __init__(self, data_dir: Union[str, pathlib.Path], recursive_exploration: bool = False):
        self._data_dir = pathlib.Path(data_dir).resolve()
        self._recursive_exploration = recursive_exploration
        self._filenames = []
        self._graphs = {}
        self._combined_graph = rdflib.Graph()
        self.update()

    @property
    def data_dir(self) -> pathlib.Path:
        """Returns the data directory where files are stored."""
        return self._data_dir

    def update(self):
        for _ext in self._expected_file_extensions:
            if self._recursive_exploration:
                self._filenames.extend([f.resolve().absolute() for f in self.data_dir.rglob(f"*{_ext}")])
            else:
                self._filenames.extend([f.resolve().absolute() for f in self.data_dir.glob(f"*{_ext}")])
        self._filenames = list(set(self._filenames))  # remove duplicates
        for filename in self._filenames:
            self._add_to_graph(filename)

    @property
    def filenames(self):
        """Returns the list of filenames uploaded to the store."""
        return self._filenames

    def upload_file(self, filename) -> bool:
        filename = pathlib.Path(filename).resolve().absolute()
        if not filename.exists():
            raise FileNotFoundError(f"File {filename} not found.")
        if filename.suffix not in self._expected_file_extensions:
            raise ValueError(f"File type {filename.suffix} not supported.")
        if filename in self._filenames:
            self._filenames.remove(filename)
        self._filenames.append(filename)
        if filename.parent != self.data_dir:
            shutil.copy(filename, self.data_dir / filename.name)
        self._add_to_graph(filename)
        return True

    def _add_to_graph(self, filename: pathlib.Path):
        """Adds the RDF graph from the file to the combined graph."""
        g = self._graphs.get(filename, None)
        if not g:
            g = rdflib.Graph()
            try:
                g.parse(filename)
            except Exception as e:
                raise ValueError(f"Could not parse file '{filename}'. Error: {e}")
            for s, p, o in g:
                if isinstance(s, rdflib.BNode):
                    new_s = rdflib.URIRef(f"https://example.org/{s}")
                else:
                    new_s = s
                if isinstance(o, rdflib.BNode):
                    new_o = rdflib.URIRef(f"https://example.org/{o}")
                else:
                    new_o = o
                g.remove((s, p, o))
                g.add((new_s, p, new_o))
            self._graphs[filename] = g
            self._combined_graph += g

    @property
    def graph(self) -> rdflib.Graph:
        return self._combined_graph
