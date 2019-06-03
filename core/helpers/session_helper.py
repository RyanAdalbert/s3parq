from core.constants import ENVIRONMENT, FORCE_POSTGRES
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as config
from sqlalchemy.orm.session import Session
from core.logging import LoggerMixin

class SessionHelper(LoggerMixin):
    """ Gets the correct env-based configuration secret,
        returns a session to the right configuration db. 
        For the dev env it pre-populates the database with helper seed data.
    """

    def __init__(self):
        self._session = None
        self.logger.info(f"Creating session for {ENVIRONMENT} environment...")  
        if ENVIRONMENT in ("prod", "uat") or FORCE_POSTGRES:
            engine = config.GenerateEngine().get_engine()
            session = config.Session(engine)
            self._session = session.get_session()
            self.logger.info(f"Done. Created {ENVIRONMENT} session.")
        elif ENVIRONMENT == "dev":
            cmock = CMock()
            cmock.generate_mocks()
            self._session = cmock.get_session()
            self.logger.info("Done. Created dev session with mock data.")  

    @property
    def session(self)-> Session:
        return self._session

    @session.setter
    def session(self, session)->None:
        raise ValueError("session cannot be explicitly set in session_helper.")
