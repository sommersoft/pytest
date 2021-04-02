#!/bin/sh

echo $(pwd)

ls -g

python -m downstream_runner $DS_YAML $DS_JOBS $DS_EXCLUDE