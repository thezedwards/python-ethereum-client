#!/usr/bin/env python
__copyright__ = "2018 QChain Inc. All Rights Reserved."
__license__ = "License: Apache v2, see LICENSE."

'''
    setup
    _____
'''

from setuptools import setup
import os
import unittest

DESCRIPTION = 'Python client for Ethereum JSON RPC API.'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Framework :: AsyncIO',
]

def test_suite():
    os.environ['REQUESTS_MOCK'] = '1'
    loader = unittest.TestLoader()
    suite = loader.discover('test', pattern='test_*.py')
    return suite


setup(
    name='python-ethereum-client',
    version='0.1.0',
    description=DESCRIPTION,
    classifiers=CLASSIFIERS,
    author='Alex Huszagh',
    author_email='ahuszagh@qchain.co',
    packages=['ethrpc'],
    url='https://github.com/q-chain/python-ethereum-client',
    license='Apache v2',
    test_suite='setup.test_suite',
    zip_safe=True,
    install_requires=[
        'bidict',
        'pycryptodome',
        'requests==2.18.4',
        'six',
    ],
    test_requires=[
        'requests-mock==1.4.0',
    ],
)
