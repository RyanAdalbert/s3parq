# 
from core.helpers.session_helper import SessionHelper as SHelp
from core.models.configuration import{
    PharmaceuticalCompany
    Brand,
    Pipeline,
    PipelineState
    Transformation,
    TransformationTemplate
}
from core.dataset_contract import DatasetContract

def contract_from_id(t_id: int):
    sess = SHelp().session
    transform = sess.query(Transformation).get(t_id)
    dataset = transform.transformation_template.name
    parent = transform.pipeline_state.pipeline.brand.pharmaceutical_company.name
    state = transform.pipeline_state.name
    child = transform.pipeline_state.pipeline.brand.name
    return DatasetContract(parent=parent, child=child, state=state, dataset=dataset)

''' waiting for Ethan's changes to config
def contract_from_name(t_name: str, contract:DatasetContract):
    sess = SHelp.session
    template = sess.query(TransformationTemplate).filter(TransformationTemplate.name)
    dataset = template.name
    #state = template.state
    #return DatasetContract(parent=contract.parent, child=contract.child, state=state, dataset=dataset)
'''