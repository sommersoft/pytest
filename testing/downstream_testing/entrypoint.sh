#!/bin/bash

groups $USER

groups postgres

python3.9 -m pip install --no-cache-dir pyyaml

/etc/init.d/postgresql start
pg_isready
psql --command "CREATE USER $USER WITH CREATEDB"

python3.9 -u -m testing.downstream_testing.downstream_runner $INPUT_DS_NAME $INPUT_DS_YAML $INPUT_DS_JOBS --matrix-exclude $INPUT_DS_MATRIX_EXCLUDE