#!/bin/sh

set -eu

cd ${GITHUB_WORKSPACE}

make lint
