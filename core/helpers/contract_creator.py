# 
from core.helpers.session_helper import SessionHelper as SHelp
from core.models.configuration import (
    PharmaceuticalCompany,
    Brand,
    Pipeline,
    PipelineState,
    Transformation,
    TransformationTemplate
)
from core.dataset_contract import DatasetContract

# Constructs and returns a dataset_contract using the parameters associated with a specified Transformation Config DB ID.
def contract_from_transformation_id(t_id: int)->DatasetContract:
    sess = SHelp().session
    transform = sess.query(Transformation).get(t_id)
    if transform is None:
        raise KeyError("Error: No transform found with id " + str(t_id))
    dataset = transform.transformation_template.name
    parent = transform.pipeline_state.pipeline.brand.pharmaceutical_company.name
    state = transform.pipeline_state.pipeline_state_type.name
    child = transform.pipeline_state.pipeline.brand.name
    return DatasetContract(parent=parent, child=child, state=state, dataset=dataset)

# Returns a contract corresponding to a specified transformation name relative to an existing contract.
# The parent/child (pharma/brand) info for the returned contract is populated from the extant contract, typically the one used to construct a DatasetDiff.
def get_relative_contract(t_name: str, contract:DatasetContract)->DatasetContract:
    sess = SHelp().session
    template = sess.query(TransformationTemplate).filter(TransformationTemplate.name==t_name).first()
    if template is None:
        raise KeyError("Error: No transform found with name " + t_name)
    dataset = template.name
    state = template.pipeline_state_type.name 
    return DatasetContract(parent=contract.parent, child=contract.child, state=state, dataset=dataset) 