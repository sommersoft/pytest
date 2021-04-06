#!/bin/bash

echo $PG_VERSION

python3.9 -m pip install --no-cache-dir pyyaml

/postgres_entrypoint.sh postgres >logfile 2>&1 &

python3.9 -u -m testing.downstream_testing.downstream_runner $INPUT_DS_NAME $INPUT_DS_YAML $INPUT_DS_JOBS --matrix-exclude $INPUT_DS_MATRIX_EXCLUDE
