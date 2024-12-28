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

### Abstractions

The package provides the following abstractions:
- `GenericLinkedDatabase`: The unified interface to interact with the semantic metadata and raw data storage
- `RDFStore`: The interface to interact with the semantic metadata storage
- `RawDataStore`: The interface to interact with the raw data storage
- `DataStoreManager`: The manager to interact with the different data stores
- `Query`: The interface to interact with the different data stores
- `RDFStoreQuery`: The interface to interact with the semantic metadata storage
- `RawDataStoreQuery`: The interface to interact with the raw data storage

### Class Diagram

```mermaid
classDiagram
    class GenericLinkedDatabase {
        <<abstract>>
        +StoreManager store_manager
        +linked_upload(filename)
        +execute_query(store_name, query)
    }

    class DataStoreManager {
        +stores: Dict
        +add_store(store_name, store)
        +get_store(store_name)
        +execute_query(store_name, query)
        +upload_file(store_name, filename)
    }

    class DataStore {
        <<abstract>>
        +execute_query(query)
        +upload_file(filename)
    }

    class RDFStore {
        <<abstract>>
        +execute_query(query)
        +upload_file(filename)
    }

    class RawDataStore {
        <<abstract>>
        +execute_query(query)
        +upload_file(filename)
    }

    class Query {
        <<abstract>>
        +execute(*args, **kwargs)
    }

    class RDFStoreQuery {
        <<abstract>>
    }

    class RawDataStoreQuery {
        <<abstract>>
    }
    
    class SparqlQuery {
        +sparql_query: str
        +execute(graph: rdflib.Graph)
    }

    %% Relationships
    GenericLinkedDatabase --> DataStoreManager
    GenericLinkedDatabase --> Query
    DataStoreManager --> DataStore
    DataStore <|-- RDFStore
    DataStore <|-- RawDataStore
    Query <|-- RDFStoreQuery
    Query <|-- RawDataStoreQuery
    RDFStoreQuery <|-- SparqlQuery : implements
```

### Workflow


## TODO:

- [ ] Add documentation
- [ ] Finish readme