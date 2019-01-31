from sqlalchemy.orm.session import Session

class SessionHelper:
    """ Gets the correct env-based configuration secret,
        returns a session to the right configuration db. 
    """
    def __init__(self):

        self.__session = None

    def get_session(self)-> Session:
        ##TODO: get @property working with magic mocks
        return self.__session
