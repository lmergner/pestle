"""
Tools to manage sqlalchemy sessions in a web application
"""

from contextlib import AbstractContextManager
import os
import logging
from sqlalchemy import event, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool


logger = logging.getLogger('pestle')


class SessionManager(AbstractContextManager):
    """ Scoped session manager """

    _engine_args = dict(
        poolclass = NullPool,
        echo = False,
        echo_pool = False,
        convert_unicode = True,
        connect_args = {},  # passed to psycopg2 
    )
    _engine = None

    def __init__(self, url, **engine_args):
        self.url = url
        self._engine_args.update(engine_args)
        self.sessionmaker = scoped_session(sessionmaker(bind=self.engine))
    
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.url)

    def __enter__(self):
        return self.sessionmaker()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            logger.error(exc_val)
        self.sessionmaker.remove()
        return (exc_val is not None)

    @property
    def engine(self):
        # https://github.com/mitsuhiko/flask-sqlalchemy/blob/50944e77522d4aa005fc3c833b5a2042280686d3/flask_sqlalchemy/__init__.py#L551
        # Note: Disable pooling using NullPool. This is the most simplistic, one shot
        # system that prevents the Engine from using any connection more than once.
        # https://docs.sqlalchemy.org/en/latest/faq/connections.html#how-do-i-use-engines-connections-sessions-with-python-multiprocessing-or-os-fork

        if not self._engine:
            self._engine = create_engine(self.url, **self._engine_args)
            if self._engine_args['poolclass'] != NullPool:
                self.add_engine_pidguard()
            
        return self._engine

    def add_engine_pidguard(self):
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
