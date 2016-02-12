#!/usr/bin/env bash
# Exit on first error and echo commands
set -e
set -x

# Run our linter and tests
flake8 *.py test/*.py
python setup.py test $*
