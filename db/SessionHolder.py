from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


class SessionHolder:
    def __init__(self, engine):
        self._session = None
        self.engine = engine
        self.create_session()

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self._session = Session()

    @property
    def session(self):
        return self._session
