#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Luke Mergner'

import argparse
import os

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pestle import models

url = os.environ.get('DATABASE_URL', None)
parser = argparse.ArgumentParser(prog='pestle-cli')
parser.add_argument('-d', '--dbname', default=url, help="postgres uri")

args = parser.parse_args()

engine = create_engine(args.dbname)
# Session = sessionmaker(bind=engine)

Base = declarative_base(cls=models.Mixin)

class Simple(Base):
    __tablename__ = 'simple'

class Post(models.Searchable, Base):
    __tablename__ = 'post'

class User(models.Admin, Base):
    __tablename__ = 'user'

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print(f'\nCheck it out:\n\t $ psql --dbname {url}')