#!/bin/sh

# Script to exec commands in GitHub Actions

set -eu

echo hi

echo adding make...
apk add make

echo make "$@"
make "$@"
