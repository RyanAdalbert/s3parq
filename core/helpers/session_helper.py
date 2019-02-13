from core.constants import ENVIRONMENT
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as config
from sqlalchemy.orm.session import Session

class SessionHelper:
    """ Gets the correct env-based configuration secret,
        returns a session to the right configuration db. 
        For the dev env it pre-populates the database with helper seed data.
    """
    def __init__(self):
        self._session = None
        if ENVIRONMENT == "dev":
            cmock = CMock()
            cmock.generate_mocks()
            self._session == cmock.get_session()
        if ENVIRONMENT in ("prod", "uat"):
            engine = config.GenerateEngine().get_engine()
            session = config.Session(engine)
            self._session = session.get_session()

    @property
    def session(self)-> Session:
        return self._session

    @session.setter
    def session(self,session)->None:
        raise ValueError("session cannot be explicitly set in session_helper.")
