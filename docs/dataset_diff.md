# dataset_diff.py

### What does it do?
`dataset_diff` takes two transformations of a given pipeline and returns all values present in the _first_ dataset but not the _second_ over a partition. Diff values are returned in a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) -- that is, values present in both transforms are excluded. This can be useful to quickly isolate unexpected behaviors between individual transformations.

### How do I use it?
First, construct a `DatasetDiff` object. The construction of `DatasetDiff` takes a single argument: 

* `transformation_id`: The unique numerical ID of the transformation to use as the base dataset.

 The transformation used to construct `DatasetDiff` should be applied earlier in the pipeline than the transformations it will diff with. If no transformation with the given ID exists, DatasetDiff will raise a `KeyError` exception.

DatasetDiff has a single method, `get_diff()`. `get_diff()` takes up to 2 arguments: 

* `transform_name`: The name of the transformation to diff against the DatasetDiff transformation.
* `value`: The values to compare `partition` to using the `comparison` operator. This is a list of one or more values with type matching the `partition` datatype
* `partition`: (_optional_) The name of the partition to return. By default, this partition is `__metadata_run_id`, a partition created for all datasets set during a RunEvent.
* `comparison`: (_optional_) The type of operation to use between `part_vals` and the values found in `partition`. Specify using string arguments ">", ">=", etc. By default, comparison is set to "==".

`get_diff()` returns a pandas DataFrame containing all values in `transform_name` filtered based on a diff partition. This partition will usually be a `run_id` which is incremented each DAG run.