#!/bin/bash

set -eu
PYTHON=python3.9

if ! command -v $PYTHON 2> /dev/null; then
    brew install python@3.9
fi

exec pipenv install