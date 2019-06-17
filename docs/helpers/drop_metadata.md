# drop_metadata.py

### What is it?
Every dataset in CORE contains some metadata fields implicitly created by CORE. This module drops those fields from a dataset, usually to be published externally where metadata fields are undesirable.

### How do I use it?
drop_metadata has a single function, drop_metadata(). It takes a single argument, `df`, a pandas DataFrame fetched from a CORE DatasetContract. This function returns the same dataset after all `__metadata` columns have been dropped.