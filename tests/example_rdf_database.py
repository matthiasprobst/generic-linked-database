import pathlib

import rdflib

from gldb import RDFStore


class InMemoryRDFDatabase(RDFStore):

    def __init__(self):
        self._filenames = []
        self._graphs = {}

    def upload_file(self, filename):
        filename = pathlib.Path(filename)
        assert filename.exists(), f"File {filename} does not exist."
        self._filenames.append(filename.resolve().absolute())

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
