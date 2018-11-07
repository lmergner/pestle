#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup


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
    description="A collection of ORM mixins and snippet for SQLAlchemy projects",
    install_requires=[
        'sqlalchemy=>1.2',
        
    ],
    license="MIT license",
    long_description='TODO',
    include_package_data=True,
    keywords='sqlalchemy',
    name='pestle',
    packages=['pestle'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/lmergner/pestle',
    version='0.1.0',
    zip_safe=False,
)
