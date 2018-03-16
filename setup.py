##
# Copyright (c) 2008-present MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from setuptools import setup


setup(
    name='edgedb-docs',
    description='EdgeDB Documentation',
    author='MagicStack Inc.',
    author_email='hello@magic.io',
    packages=['edgedb.sphinxext'],
    provides=['edgedb.sphinxext'],
    include_package_data=True,
    test_suite='tests.suite',
)
