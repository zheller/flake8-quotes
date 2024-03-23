#!/usr/bin/env bash
# Exit on first error and echo commands
set -e
set -x

# Run our linter and tests
flake8 *.py flake8_quotes/ test/*.py
pytest
