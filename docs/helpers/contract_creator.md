# contract_creator.py

### What does it do?
contract_creator is a module which can construct `DatasetContracts` one of two ways: from a transformation ID corresponding to a valid transformation in the configuration DB, or from a transformation name coupled with a valid DatasetContract in the same pipeline. Although contract_creator is intended as a helper for `DatasetDiff`, you can also call it directly.

### How do I use it?
contract_creator has two methods, `contract_from_transformation_id()` and `get_relative_contract()`. 

contract_from_transformation_id takes a single argument, `t_id`, an int corresponding to the Transformation (_not_ TransformationTemplate) ID in the configuration DB. Everything needed to construct a DatasetContract can be accessed relatively via this t_id. Example usage:

```
import core.helpers.contract_creator as cc
absolute_contract = cc.contract_from_transformation_id(t_id=4)
```

get_relative_contract takes two arguments: `t_name`, the name of the transformation & dataset, and `contract`, another contract sharing a pipeline with `t_name`. Example usage:

```
import core.helpers.contract_creator as cc
absolute_contract = cc.contract_from_transformation_id(t_id=4)
relative_contract = cc.get_relative_contract(t_name="my_transform_name", contract=absolute_contract) # relative_contract and absolute_contract must belong to the same pipeline
```