#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Luke Mergner"

import argparse
import os

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pestle import models

url = os.environ.get("DATABASE_URL", None)
parser = argparse.ArgumentParser(prog="pestle-cli")
parser.add_argument("-d", "--dbname", default=url, help="postgres uri")

args = parser.parse_args()

engine = create_engine(args.dbname)
# Session = sessionmaker(bind=engine)

Base = declarative_base(cls=models.Mixin)


class Simple(Base):
    __tablename__ = "simples"


class Post(models.Searchable, Base):
    __tablename__ = "posts"


class User(models.PasswordAuth, Base):
    __tablename__ = "users"


class ApiUser(models.TokenAuth, Base):
    __tablename__ = "api_users"


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print(f"\nCheck it out:\n\t $ psql --dbname {url}")
