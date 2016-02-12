#!/usr/bin/env bash
# Exit on first error
set -e

# Parse our CLI arguments
version="$1"
if test "$version" = ""; then
  echo "Expected a version to be provided to \`release.sh\` but none was provided." 1>&2
  echo "Usage: $0 [version] # (e.g. $0 1.0.0)" 1>&2
  exit 1
fi

# All references to a version number are derived from this file.
echo "$version" > VERSION

# Commit the change
git add flake8_quotes.py
git commit -a -m "Release $version"

# Tag the release
git tag "$version"

# Publish the release to GitHub
git push
git push --tags

# Publish the release to PyPI
python setup.py sdist --formats=gztar,zip upload
