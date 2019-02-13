from core.constants import ENVIRONMENT
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from sqlalchemy.orm.session import Session

class SessionHelper:
    """ Gets the correct env-based configuration secret,
        returns a session to the right configuration db. 
    """
    def __init__(self):
        self._session = None
        if ENVIRONMENT == "dev":
            cmock = CMock()
            cmock.generate_mocks()
            self._session = cmock.get_session()
        elif ENVIRONMENT == "prod":
            pass

    @property
    def session(self)-> Session:
        return self._session

    @session.setter
    def session(self,session)->None:
        raise ValueError("session cannot be explicitly set in session_helper.")
