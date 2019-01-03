#!/bin/sh

# Script to exec commands in GitHub Actions

set -eu

echo Adding make...
echo
apk add make
echo
echo

sh -c "$@"
