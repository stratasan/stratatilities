#!/bin/sh
set -eu
# Script to exec commands in GitHub Actions

date
echo Adding make...
echo
apk add make
echo
echo

date
echo Exeucting "$*"
sh -c "$*"
