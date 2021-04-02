#!/bin/sh

find -path **/*.yml

which python

cd $GITHUB_WORKSPACE

python -m downstream_runner $DS_YAML $DS_JOBS $DS_EXCLUDE