from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from core.helpers.session_helper import SessionHelper
from core.models.configuration import Pipeline, Transformation, PipelineState

def __get_or_create(session:Session, model, find:dict, populate:dict):
    """ finds the model instance or creates it.
        ARGS:
            session: the sqlaclhemy db session
            model: the model class to look up 
            find: the key value dict to look up existing instance with
            populate: the key values to populate a new instance with (in addition to the find values)
        RETURNS: model instace of the found/created class 
    """
    try:
        if len(find.keys()) == 1:
            return session.query(model).filter_by(**find).one()
        else:
            query = session.query(model)
            for k,v in find.items():
                query = query.filter_by(k=v)
            return query.one()

    except NoResultFound:
        model_args = find.update(populate)
        new_model = model(**model_args)
        session.add(new_model)
        return new_model