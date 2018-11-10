# -*- coding: utf-8 -*-

""" pestle.models

Mixin and other helpers for SQLAlchemy
"""
# https://sqlalchemy-utils.readthedocs.io/
# https://github.com/openstack/sqlalchemy-migrate

import uuid

from passlib.context import CryptContext
from sqlalchemy import (
    DDL,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    create_engine,
    event,
    exc,
    types,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression


NAMING_CONVENTION={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class utcnow(expression.FunctionElement):
    type = types.DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Mixin:
    """ Base class for SQLAlchemy models

    usage:

    >>> Base = declarative_base(cls=Mixin)
    """
    __abstract__ = True

    # TODO: implement query_property with session lazy loading

    # Housekeeping
    oid = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=utcnow())
    modified = Column(
        DateTime(timezone=True), onupdate=utcnow(), server_default=utcnow()
    )
    extras = Column(postgresql.JSON, default={})

    def __repr__(self):
        return "<{name}({oid})>".format(
            name=self.__tablename__, oid=self.oid or "dirty"
        )


class Searchable:
    """ An SQLAlchemy ORM mixin that provides a searchable interface using Postgres TSVECTOR columns 
    
    :example:
    >>> class Text(Searchable, Base):
    >>>     pass
    
    """
    # Original inspiration: http://shisaa.jp/postset/postgresql-full-text-search-part-1.html
    # __abstract__ = True

    _trigger_ddl = (
        # TODO: customize the trigger name
        "create trigger ts_update before insert or update on {tablename} for "
        "each row execute procedure tsvector_update_trigger(tsvector, "
        "'pg_catalog.english', 'text');"
    )

    # Data Fields
    text = Column(String)

    # PostgreSQL Full Text Search field
    # http://www.postgresql.org/docs/current/static/datatype-textsearch.html
    # TODO:  needs tests for on_update hook
    tsvector = Column(postgresql.TSVECTOR)

    @declared_attr
    def __table_args__(cls):
        # Must return a tuple
        return (
            # CREATE INDEX tsvector_idx ON feedback USING gin(to_tsvector('english', message));
            Index(
                "tsvector_idx_%s" % cls.__tablename__,
                "tsvector",
                postgresql_using="gin",
        ), {
            # Per Mike Bayer
            # https://groups.google.com/d/msg/sqlalchemy/CrjqfxdEOyM/7WnZ80HgAwAJ
            "listeners": [("after_create", DDL(cls._trigger_ddl.format(tablename=cls.__name__)).execute_if(dialect="postgresql"))]
        })


class Admin:
    """ Admin mixin """

    # passlib will auto-update any plaintext passwords
    _pass_context = CryptContext(
        schemes=["bcrypt", "plaintext"],
        default="bcrypt",
        deprecated=["plaintext"],
        bcrypt__min_rounds=13,
    )
    token = Column(String, unique=True, default=None)
    token_updated = Column(DateTime(timezone=True))
    _password = Column("password", String)
    password_updated = Column(DateTime(timezone=True))

    def verify_password(self, password):
        """ verify a password using passlib """
        valid, new_hash = self._pass_context.verify_and_update(password, self._password)
        if valid:
            if new_hash:
                self._password = new_hash
                self.password_updated = utcnow()
            return True
        return False

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        # TODO:  support for expiring passwords
        self._password = self._pass_context.encrypt(password)
        self.password_updated = utcnow()

    def generate_token(self):
        # TODO:  support for expiring tokens      
        self.token = uuid.uuid4().hex
        self.token_updated = utcnow()
        return self.token
