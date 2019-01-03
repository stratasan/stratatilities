#!/bin/sh

# Script to exec commands in GitHub Actions

set -eu

echo Adding make...
echo
apk add make
echo
echo

echo Installing black...
echo
pip install black
echo
echo

echo Make "$@"
make "$@"
