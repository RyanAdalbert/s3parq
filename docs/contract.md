# Contract
The contract class defines the way we write to and read from the S3 data lake. It offers us an abstraction from directly writing to the filesystem, so we inject RDBMS-like structure to what is essentially a raw file store. 

## Standard Structure
    *--------------------------------------------------------------------------------------------------------------------*
    | contract structure in s3:                                                                                          |
    |                                                                                                                    |
    | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} / {DATASET} / {PARTITION} [ / {SUB-PARTITION} / ] {FILENAME} |
    |                                                                                                                    |
    *--------------------------------------------------------------------------------------------------------------------*

This is enforced by using `getter` and `setter` arguments - i.e. `get\_state()` to retrieve a contract state, `set\_state('raw')` to set the state.
_TODO:_ we want to migrate these to `@property` python attributes. 
    

### Writing to S3
Invoke the `publish()` command to write to a given contract. Some things to know:
- To invoke publish a contract must be at the grain of dataset. This is because file names will be set by the dataframe=\>parquet conversion. 
- publish only accepts a pandas dataframe.
- publish does not allow for timedelta data types at this time (this is missing functionality in pyarrow).
- publish handles partitioning the data as per contract, creating file paths, and creating the binary parquet files in S3, as well as the needed metadata.

### Reading from S3
Invoke the `fetch()` command to query a given contract. Some things to know:
- To invoke fetch a contract must be at the grain of dataset. This is because file names and partitions to read from will be set by the command params.
- fetch allows for basic filtering on partitioned columns only. 
- fetch returns a single pandas dataframe based on the filter criterion. 



**Notables**:
get\_brand() and get\_child() are synonymous.
get\_customer() get\_parent() are synonymous.
get\_contract\_type() tells you the scope of the contract (state, dataset, or file)
get\_key() gives you the AWS "key" value (file without bucket)
get\_next\_state() and get\_previous\_state() refer to the standard transform order raw-\> dimensional
get\_partition\_size() returns the number of MB for each partition (pre-compression)
get\_partitions() returns a list of data partitions, in order
get\_s3\_path() returns the full s3 path
publish\_raw\_file() will put a local file on S3 in the raw state for the current contract
    
