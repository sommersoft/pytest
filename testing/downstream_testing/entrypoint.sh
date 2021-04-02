#!/bin/sh

ls

find -name *.yml

python -V

python -m downstream_runner $DS_YAML $DS_JOBS $DS_EXCLUDE