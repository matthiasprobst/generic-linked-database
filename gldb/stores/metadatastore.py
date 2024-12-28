import json
import pathlib
from abc import ABC, abstractmethod
from typing import Union

import rdflib

from .store import DataStore


class RDFStore(DataStore, ABC):
    """Graph database interface."""

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

    @abstractmethod
    def upload_file(self, filename: Union[str, pathlib.Path]) -> bool:
        """Insert data into the data store."""
        pass

    def select(self, item: str, serialization_format="json-ld", **kwargs) -> str:
        if item.startswith("http"):
            _item = f"<{item}>"
        else:
            prefix, name = item.split(":", 1)
            _item = f"<{self.namespaces[prefix]}{name}>"

        prefixes = "\n".join([f"PREFIX {k}: <{v}>" for k, v in self.namespaces.items()])
        sparql_query = f"{prefixes}\nSELECT * WHERE {{ {_item} ?p ?o }}"

        result = self.graph.query(sparql_query)
        result_data = [{str(k): v for k, v in binding.items()} for binding in result.bindings]
        metadata = {d["p"]: d["o"] for d in result_data}

        g = rdflib.Graph()
        for k, v in metadata.items():
            if isinstance(v, str) and v.startswith("http"):
                v = rdflib.URIRef(v)
            g.add((rdflib.URIRef(item), rdflib.URIRef(k), v))

        if "context" in kwargs:
            _context = self.namespaces.copy()
            _context.update(kwargs["context"])
            kwargs["context"] = _context
        else:
            kwargs["context"] = self.namespaces

        serialized = g.serialize(format=serialization_format, **kwargs)
        if serialization_format == "json-ld":
            deserialized = json.loads(serialized)
            for k, v in deserialized.items():
                if isinstance(v, dict):
                    if len(v) == 1 and "@id" in v:
                        deserialized[k] = v["@id"]
            return json.dumps(deserialized, indent=kwargs.get("indent", None))
        return serialized
