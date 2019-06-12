# Contract
The DatasetContract class defines the way we write to and read from the S3 data lake. It offers us an abstraction from directly writing to the filesystem, so we inject RDBMS-like structure to what is essentially a raw file store. 

## Standard Structure
    *--------------------------------------------------------------------------------------------------------------------*
    | dataset contract structure in s3:                                                                                  |
    |                                                                                                                    |
    | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} / {DATASET} / {PARTITION} [ / {SUB-PARTITION} / ] {FILENAME} |
    |                                                                                                                    |
    *--------------------------------------------------------------------------------------------------------------------*

    *--------------------------------------------------------------------------------------------------------------------*
    | dataset contract structure in CORE (core/dataset_contract.py):                                                    |
    |                                                                                                                    |
    | bucket: {ENV}                                                                                                      |
 	| key: {BRANCH} / {PARENT} / {CHILD} / {STATE} / {DATASET}                                                           |
    |                                                                                                                    |
    *--------------------------------------------------------------------------------------------------------------------*

Make sure that you are using DatasetContract and not Contract. Contract is a parent class DatasetContract inherits from and should not be used directly.

Properties of DatasetContracts can be retrieved as attributes, e.g. {contract\_name}.parent

### Writing to S3
Invoke the `publish()` command to write to a given contract. Some things to know:
- To invoke publish a contract must be at the grain of dataset. This is because file names will be set by the dataframe=\>parquet conversion. 
- publish only accepts a pandas dataframe.
- publish does not allow for timedelta data types at this time (this is missing functionality in pyarrow).
- publish handles partitioning the data as per contract, creating file paths, and creating the binary parquet files in S3, as well as the needed metadata.

### Reading from S3
Invoke the `fetch()` command to query a given contract. Some things to know:
- fetch requires params `bucket` and `key`. Each contract has attributes `bucket` and `key` which can be passed directly as the values for fetch.
- To invoke fetch a contract must be at the grain of dataset. This is because file names and partitions to read from will be set by the command params.
- fetch allows for basic filtering on partitioned columns only.
- fetch returns a single pandas dataframe based on the filter criterion.
- see `docs/dataset_diff.md` for retrieving the diff of 2 datasets.

### Partitioning Datasets
Invoke the `partitions()` command to set partitions for a given contract. Some things to know:
- partitions requires a parameter `partitions`, a list of column names to partition on. Partitions are applied in the order they appear in the list.
- by default, all datasets include a single partition, \_\_metadata\_run\_timestamp. 

**Notables**:
{dataset\_contract}.bucket returns the bucket part of the dataset contract structure (usually just the environment).
{dataset\_contract}.key returns the key part of the dataset contract structure.
{dataset\_contract}.brand and {dataset_contract}.child are synonymous.
{dataset\_contract}.customer {dataset_contract}.parent are synonymous.
{dataset\_contract}.contract_type tells you the scope of the contract (state, dataset, or file).
{dataset\_contract}.next\_state and {dataset\_contract}.previous\_state return the next and previous state according to [this standard](https://integrichain.atlassian.net/wiki/spaces/Core/pages/722731374/Marketecture+Core+Contract).
{dataset\_contract}.s3\_path() returns the full s3 path.
    
