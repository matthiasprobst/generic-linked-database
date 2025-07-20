import pathlib

import rdflib

from gldb.stores import RDFStore


class InMemoryRDFDatabase(RDFStore):

    def __init__(self):
        self._filenames = []
        self._graphs = {}
        self._expected_file_extensions = {".ttl", ".rdf", ".jsonld"}

    @property
    def expected_file_extensions(self):
        return self._expected_file_extensions

    # def execute_query(self, query: SparqlQuery):
    #     return query.execute(self.graph)

    def upload_file(self, filename) -> bool:
        filename = pathlib.Path(filename)
        if not filename.exists():
            raise FileNotFoundError(f"File {filename} not found.")
        if filename.suffix not in self._expected_file_extensions:
            raise ValueError(f"File type {filename.suffix} not supported.")
        self._filenames.append(filename.resolve().absolute())
        return True

    @property
    def graph(self) -> rdflib.Graph:
        combined_graph = rdflib.Graph()
        for filename in self._filenames:
            g = self._graphs.get(filename, None)
            if not g:
                g = rdflib.Graph()
                g.parse(filename)
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
            combined_graph += g
        return combined_graph
