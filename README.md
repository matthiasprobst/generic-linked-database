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
  graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
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