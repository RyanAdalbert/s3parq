# dataset_diff.py

### What does it do?
`dataset_diff` takes two transformations of a given pipeline and returns all values present in the _first_ dataset but not the _second_ over a partition. Diff values are returned in a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) -- that is, values present in both transforms are excluded. This can be useful to quickly isolate unexpected behaviors between individual transformations.

### How do I use it?
First, construct a `DatasetDiff` object. The construction of `DatasetDiff` takes a single argument: the unique numerical ID of the transformation to use as the base dataset. This transformation should be applied earlier in the pipeline than the transformations it will diff against. If no transformation with the given ID exists, DatasetDiff will raise a `KeyError` exception.

DatasetDiff has a single method, `get_diff()`. `get_diff()` takes 2 arguments: 

* `transform_name`: the name of the transformation to diff against the DatasetDiff transformation
* `partition`: (_optional_) the name of the partition to return. By default, this partition is `__metadata_run_timestamp`, a partition created for all datasets.

`get_diff()` returns a pandas DataFrame containing all values in the transformation constructed with DatasetDiff not present in the transformation specified in `get_diff()`. `get_diff()` can be run any number of times using any number of transformations, but all diffs will compare against DatasetDiff's constructed transformation.