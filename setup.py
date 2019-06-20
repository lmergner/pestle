#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author="Luke Thomas Mergner",
    author_email='lmergner@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="An opinionated collection of ORM mixins and tools for SQLAlchemy projects",
    install_requires=[
        'sqlalchemy==1.3.5',
        'passlib==1.7.1',
        'bcrypt==3.1.7',
        'psycopg2-binary==2.8.3',
    ],
    license="MIT license",
    long_description=long_description,
    keywords='sqlalchemy',
    name='pestle',
    packages=['pestle'],
    test_suite='tests',
    tests_require=[
        'pytest==4.6.3',
        'pytest-cov==2.7.1',
        'pytest-pgtap @ git+https://github.com/lmergner/pytest-pgtap@v0.1.0#egg=pytest_pgtap',  # https://github.com/pypa/pip/issues/3939
    ],
    setup_requires=["pytest-runner"],
    url='https://github.com/lmergner/pestle',
    version='0.1.1',
    zip_safe=False,
)
