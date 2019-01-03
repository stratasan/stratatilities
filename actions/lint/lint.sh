#!/bin/sh

set -eu

cd ${GITHUB_WORKSPACE}

# Run flake8
black --check .
