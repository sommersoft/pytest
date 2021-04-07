#!/bin/bash

echo $PG_VERSION

/postgres_entrypoint.sh postgres -D $PGDATA >/var/log/postgresql/log.txt & #2>&1 </dev/null &

#gosu postgres cat /var/log/postgresql/log.txt

#pg_isready -t 240 --port=/var/run/postgresql/.s.PGSQL.5432
#psql -l --port=/var/run/postgresql/.s.PGSQL.5432

python3.9 -m pip install --no-cache-dir pyyaml

python3.9 -u -m testing.downstream_testing.downstream_runner $INPUT_DS_NAME $INPUT_DS_YAML $INPUT_DS_JOBS --matrix-exclude $INPUT_DS_MATRIX_EXCLUDE

gosu postgres cat /var/log/postgresql/log.txt