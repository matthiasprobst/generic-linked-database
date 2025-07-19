# CHANGELOG

## v2.0.0

- major refactoring of database organisation and naming:
  - `RDFStore` renamed to `MetadataStore`
  - `GenericLinkedDatabase` is not abstract anymore, but a concrete class
  - Stores (of type `Store`) must be provided with a name when instantiating a `GenericLinkedDatabase`
  - Files are organized slightly different, so you may need to adjust your imports
  - a store must provide the query class via abstract property `query`

## v1.2.1

- update setuptools to >=78.1.1 for security reasons

## v1.2.0

- introduce `SparqlResult` as return value of query execution
- add property `description` to `Query`
- add `__str__()` method to SparqlQuery class
- removed unused `FederatedQueryResult`
- cleanup and housekeeping

## v1.1.0

- removed unnecessary abstract methods/properties, which simplifies the code