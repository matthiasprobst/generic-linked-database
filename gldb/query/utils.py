import json

from rdflib import Graph


def sparql_query_to_jsonld(graph: Graph, query: str) -> dict:
    results = graph.query(query)

    jsonld = {
        "@context": {},
        "@graph": []
    }

    for row in results:
        item = {}
        for var, value in row.asdict().items():
            if value is not None:
                if hasattr(value, 'n3'):
                    val_str = value.n3(graph.namespace_manager)
                else:
                    val_str = str(value)

                item[var] = val_str

                # Add simple context mapping
                if isinstance(value, (str, int, float)):
                    jsonld["@context"][var] = None
                elif value.__class__.__name__ == 'URIRef':
                    jsonld["@context"][var] = str(value)

        if item:
            jsonld["@graph"].append(item)

    return jsonld


if __name__ == "__main__":
    # Example usage
    g = Graph()
    g.parse(data="""
    @prefix ex: <http://example.org/> .
    ex:subject1 ex:predicate1 "object1" .
    ex:subject2 ex:predicate2 "object2" .
    """, format="turtle")

    query = """
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
    }
    """
    jsonld_result = sparql_query_to_jsonld(g, query)
    print(json.dumps(jsonld_result, indent=2))

    query2 = """
    PREFIX ex: <http://example.org/>
    SELECT ?p ?o WHERE {
        ex:subject1 ?p ?o .
    }
    """
    jsonld_result = sparql_query_to_jsonld(g, query2)
    print(json.dumps(jsonld_result, indent=2))
