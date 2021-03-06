import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pestle import models

Base = declarative_base(cls=models.Mixin)

class Simple(Base):
    __tablename__ = 'simple'

class Post(models.Searchable, Base):
    __tablename__ = 'post'

class User(models.Admin, Base):
    __tablename__ = 'user'


@pytest.fixture(scope="session", autouse=True)
def create_tables(request):
    DATABASE_URL = request.config.option.pgtap_uri
    engine = create_engine(DATABASE_URL)
    print('Creating tables')
    Base.metadata.create_all(engine)
    yield
    print('Dropping tables')
    Base.metadata.drop_all(engine)
