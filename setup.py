# Copyright 2010 Dan Colish
# All rights reserved.
#
# This file is part of 'fusionsql' and is distributed under the BSD license.
# See LICENSE for more details.
"""
FusionSQL
=========

Client for connecting with google Fusion Tables

copyright 2010 Dan Colish <dcolish@gmail.com>

See LICENSE for more detail

* `development version
  <http://github.com/dcolish/fusionsql/zipball/master#egg=fusionsql-dev>`_
"""
from setuptools import setup, find_packages

setup(name="fusionsql",
      version="dev",
      packages=find_packages(),
      namespace_packages=['fusionsql'],
      include_package_data=True,
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      description='Fusion Tables SQL Client',
      long_description=__doc__,
      zip_safe=False,
      platforms='any',
      license='BSD',
      url='http://www.github.com/dcolish/fusionsql',

      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        ],

      entry_points={
        'console_scripts': [
            'fusionsql=fusionsql.client:run_cli',
            ],
        },

      install_requires=[
        'oauth2',
        ],

      test_suite="nose.collector",
      tests_require=[
        'nose',
        ],
      )
