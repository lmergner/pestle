#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

# TODO: convert to setup.cfg per python packaging recommendations
# TODO: move bcrypt and passlib to an extras_require stanza
setup(
    author="Luke Thomas Mergner",
    author_email="lmergner@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="An opinionated collection of ORM mixins and tools for SQLAlchemy projects",
    install_requires=[
        "sqlalchemy>=1.3.17",
        "passlib>=1.7.2",
        "bcrypt>=3.1.7",
        "gunicorn==20.0.4",
        # TODO:  psycopg should be built form source according to the docs
        "psycopg2-binary>=2.8.5",
    ],
    extras_require={
        "async": ["SQLAlchemy==1.4.0b1", "asyncpg==0.21.0", "uvloop==0.14.0"],
        "sync": [],
    },
    license="MIT license",
    long_description=long_description,
    keywords="sqlalchemy",
    name="pestle",
    packages=["pestle"],
    test_suite="tests",
    tests_require=[
        "pytest>=6.1.1",
        "pytest-cov>=2.9.0",
        "pytest-pgtap @ git+https://github.com/lmergner/pytest-pgtap@v0.1.0#egg=pytest_pgtap",
        # https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    ],
    setup_requires=["pytest-runner"],
    url="https://github.com/lmergner/pestle",
    version="0.1.3",
    zip_safe=False,
)
