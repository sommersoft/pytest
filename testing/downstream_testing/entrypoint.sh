#!/bin/sh

ls -CR

find -path **/*.yml

python -V

python -m downstream_runner $DS_YAML $DS_JOBS $DS_EXCLUDE