#!/bin/sh

echo $(pwd)

ls -g

python -c "import os; print(os.getcwd())"

python -m downstream_runner $DS_YAML $DS_JOBS $DS_EXCLUDE