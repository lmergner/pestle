from sqlalchemy.orm import scoped_session, sessionmaker

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