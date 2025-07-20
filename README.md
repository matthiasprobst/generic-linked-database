# generic-linked-database

![Tests Status](https://github.com/matthiasprobst/generic-linked-database/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/matthiasprobst/generic-linked-database/branch/main/graph/badge.svg?token=2ZFIX0Z1QW)](https://codecov.io/gh/matthiasprobst/generic-linked-database)
![pyvers Status](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)

An approach to integrate multiple databases behind a unified interface.

Consider the following scenario: You have SQL database or a file database of CSV files, however, these data are missing
metadata.
Your metadata is stored in a separate RDF database. So your actual database are in two different databases, one for the
data and one for the metadata.

Using `gldb`, you can access both databases through a unified interface. This allows you to query the data and metadata
together in a simple way.

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

