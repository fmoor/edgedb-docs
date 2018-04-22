#!/bin/bash

set -e -x

export CI_PROJECT_DIR=$TRAVIS_BUILD_DIR
export PIP_CACHE_DIR=$(pwd)/build/pip/
pip --quiet install vex
vex --python=python3 -m test pip install --quiet -U setuptools wheel pip
vex test pip install --quiet -U -r requirements.dev.txt
vex test pip install -U git+ssh://git@github.com/edgedb/edgedb.git#eggname=edgedb
vex test python setup.py test
