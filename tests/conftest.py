import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pestle import models

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base(cls=models.Mixin)

class Simple(Base):
    __tablename__ = 'simple'

class Post(models.Searchable, Base):
    __tablename__ = 'post'

class User(models.Admin, Base):
    __tablename__ = 'user'

def pytest_configure(config):
    print('Creating tables')
    Base.metadata.create_all(engine)

def pytest_unconfigure(config):
    print('Dropping tables')
    Base.metadata.drop_all(engine)