# generic-linked-database

![Tests Status](https://github.com/matthiasprobst/generic-linked-database/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/matthiasprobst/generic-linked-database/branch/main/graph/badge.svg?token=2ZFIX0Z1QW)](https://codecov.io/gh/matthiasprobst/generic-linked-database)
![pyvers Status](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)

An approach to integrate multiple databases behind a unified interface. At least on database is intended to be 
an RDF database for metadata storage, the others are raw data storages like SQL or noSQL databases.

## Quickstart

### Installation

Install the package:

```bash
pip install gldb
```

### Example

An example exists as [Jupyter Notebook](docs/examples/Tutorial.ipynb) in `docs/examples/`. You may also try it online 
with Google Colab:

[![Open Quickstart Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matthiasprobst/generic-linked-database/blob/main/docs/examples/Tutorial.ipynb)

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
        +execute_query(query) QueryResult
        +upload_file(filename)
    }

    class RawDataStore {
        <<abstract>>
        +execute_query(query) QueryResult
        +upload_file(filename)
    }

    class Query {
        +description: str
        <<abstract>>
        +execute(*args, **kwargs) QueryResult
    }

    class QueryResult {
        query: Query
        result: Any
    }

    class RDFStoreQuery {
        <<abstract>>
    }

    class RawDataStoreQuery {
        <<abstract>>
    }
    
    class SparqlQuery {
        +sparql_query: str
        +execute(graph: rdflib.Graph) QueryResult
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


