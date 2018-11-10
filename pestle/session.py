"""
Tools to manage sqlalchemy sessions in a web application


"""
import os
from contextlib import AbstractContextManager
from sqlalchemy import event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool


def add_engine_pidguard(engine):
    """Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.

    copied from the sqlalchemy docs, copyright Mike Bayer.
    """

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        connection_record.info["pid"] = os.getpid()

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info["pid"] != pid:
            # substitute log.debug() or similar here as desired
            logger.warning(
                "Parent process %(orig)s forked (%(newproc)s) with an open "
                "database connection, "
                "which is being discarded and recreated."
                % {"newproc": pid, "orig": connection_record.info["pid"]}
            )
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s"
                % (connection_record.info["pid"], pid)
            )



class Session:
    session = None

    def __init__(self, url=None):
        if url is None:
            self.url = "sqlite://insta.sql"
        else:
            self.url = url
        self._engine = create_engine(url, poolclass=NullPool)
        self._session_maker = scoped_session(sessionmaker(bind=self._engine))

    def __enter__(self):
        if not self.session:
            self.session = self._session_maker()
        return self.session

    def __exit__(self, _type, value, traceback):
        if _type:
            logger.error(value)
            self.session.rollback()
        if self.session:
            self._session_maker.remove()
            self.session = None

class SessionManager(AbstractContextManager):
    """ Session context manager """

    pool_class = NullPool

    def __init__(self, url):
        self._connected_for = None
        self._engine = self.get_engine()
        self._session_maker = scoped_session(sessionmaker(bind=self._engine))
        self.session = None

    def get_engine(self):
        # https://github.com/mitsuhiko/flask-sqlalchemy/blob/50944e77522d4aa005fc3c833b5a2042280686d3/flask_sqlalchemy/__init__.py#L551
        echo = config.SQLALCHEMY_ECHO
        uri = config.DATABASE_URL
        # Note: Disable pooling using NullPool. This is the most simplistic, one shot
        # system that prevents the Engine from using any connection more than once.
        # https://docs.sqlalchemy.org/en/latest/faq/connections.html#how-do-i-use-engines-connections-sessions-with-python-multiprocessing-or-os-fork
        self._engine = create_engine(
            uri, echo=echo, convert_unicode=True, poolclass=self.pool_class
        )
        # add_engine_pidguard(self._engine)
        return self._engine

    def __enter__(self):
        if not self.session:
            self.session = self._session_maker()
        return self.session

    def __exit__(self, _type, value, traceback):
        if _type:
            logger.error(value)
            self.session.rollback()
        if self.session:
            self._session_maker.remove()
            self.session = None