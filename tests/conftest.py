import os

import pytest
from pestle import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: does collect_ignore matter?
# https://docs.pytest.org/en/stable/example/pythoncollection.html
collect_ignore = ['setup.py']

Base = declarative_base(cls=models.Mixin)


class Simple(Base):
    __tablename__ = 'simple'


class Post(models.Searchable, Base):
    __tablename__ = 'post'


class User(models.PasswordAuth, models.TokenAuth, Base):
    __tablename__ = 'user'


class APIUser(models.TokenAuth, Base):
    __tablename__ = "apiusers"


@pytest.fixture(scope="session", autouse=True)
def create_tables(request):
    DATABASE_URL = request.config.option.pgtap_uri
    engine = create_engine(DATABASE_URL)
    print('Creating tables')
    Base.metadata.create_all(engine)
    yield
    print('Dropping tables')
    Base.metadata.drop_all(engine)
