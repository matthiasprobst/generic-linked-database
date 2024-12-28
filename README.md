# generic-linked-database

![Tests Status](https://github.com/matthiasprobst/generic-linked_database/actions/workflows/tests.yml/badge.svg)
![Coverage](https://codecov.io/gh/matthiasprobst/generic-linked_database/branch/main/graph/badge.svg)
![pyvers Status](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

An approach to integrate linked semantic metadata and raw data storage behind a unified interface

## Quickstart

### Installation

Install the package:

```bash
pip install generic-linked-database
```

## Design

```mermaid
classDiagram
    class GenericLinkedDatabase {
        <<Abstract>>
        +RDFStore rdfstore
        +DataStore datastore
        +linked_upload(filename: Union[str, pathlib.Path])
        +execute_query(query: Query)
    }

    class Store {
        <<Abstract>>
        +execute_query(query: Query)
        +expected_file_extensions
        +upload_file(filename: Union[str, pathlib.Path]): bool
    }

    class RDFStore {
        <<Abstract>>
        +rdflib.Graph graph
        +upload_file(filename: Union[str, pathlib.Path]): bool
    }

    class DataStore {
        <<Abstract>>
        +upload_file(filename: Union[str, pathlib.Path]): bool
    }

    class Query {
        <<Abstract>>
        +execute(*args, **kwargs)
    }

    class RDFStoreQuery {
        <<Abstract>>
    }

    class SparqlQuery {
        -sparql_query: str
        +execute(graph: rdflib.Graph): rdflib.query.Result
    }

    class DataStoreQuery {
        <<Abstract>>
    }

    GenericLinkedDatabase --> Store
    GenericLinkedDatabase --> RDFStore
    GenericLinkedDatabase --> DataStore
    Store <|-- RDFStore
    Store <|-- DataStore
    Query <|-- RDFStoreQuery
    Query <|-- DataStoreQuery
    RDFStoreQuery <|-- SparqlQuery

```

### Abstractions

The package provides the following abstractions:
- `GenericLinkedDatabase`: The unified interface to interact with the semantic metadata and raw data storage
- `RDFStore`: The interface to interact with the semantic metadata storage
- `DataStore`: The interface to interact with the raw data storage

The user interacts with the database and can either interact with the metadata store, the data store or via a federated 
query with both.

![Alt text](docs/figures/abstraction.svg)

### Workflow


## TODO:

- [ ] Add documentation
- [ ] Finish readme