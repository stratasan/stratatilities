#!/bin/sh -l
# Script to exec commands in GitHub Actions

set -eu
apk add make
make "$@"
