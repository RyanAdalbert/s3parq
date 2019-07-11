from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from core.helpers.session_helper import SessionHelper
from core.logging import LoggerSingleton
from random import randint
import core.helpers.postgres_toggle as pg_toggle
import core.models.configuration as config
import sys

logger = LoggerSingleton().logger

def _get_or_create(session: Session, model, find:dict):
    """ finds the model instance or creates it.
        ARGS:
            session: SQLalchemy session
            model: the model class to look up 
            find: the key value dict to look up existing instance with
        RETURNS: model instace of the found/created class 
    """
    try:
        return session.query(model).filter_by(**find).one()
    except NoResultFound:
        new_model = model(**find)
        session.add(new_model)
        session.commit()
        return new_model

def build(pharma_company: str, brand: str, state: str, transformation: str, session: Session):
    logger.debug("Adding/getting mocks for specified configurations...")
    find = dict(name=pharma_company, display_name=pharma_company)
    pc = _get_or_create(session, config.PharmaceuticalCompany, find)
    find = dict(name=brand, display_name=brand, pharmaceutical_company_id=pc.id)
    br = _get_or_create(session, config.Brand, find)
    pipeline_name = "singleton_" + transformation
    find = dict(name=pipeline_name, brand_id=br.id, pipeline_type_id=0)
    pipeline = _get_or_create(session, config.Pipeline, find)
    find = dict(name=state)
    st_type = _get_or_create(session, config.PipelineStateType, find)
    find = dict(pipeline_state_type_id=st_type.id, pipeline_id=pipeline.id, graph_order=0)
    st = _get_or_create(session, config.PipelineState, find)
    find = dict(name=transformation, pipeline_state_type_id=st_type.id)
    tt = _get_or_create(session, config.TransformationTemplate, find)
    find = dict(transformation_template_id=tt.id, pipeline_state_id=st.id, graph_order=0)
    tr = _get_or_create(session, config.Transformation, find)
    logger.debug("Done. Creating mock run event and committing results to configuration mocker.")
    run_event = config.RunEvent(id=randint(100000, 999999), pipeline_id=pipeline.id)
    session.add(run_event)
    session.commit()
    ids = [tr.id, run_event.id]
    session.close()

    return ids
