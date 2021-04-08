#!/bin/bash

echo $PG_VERSION

/postgres_entrypoint.sh postgres -D $PGDATA >/var/log/postgresql/log.txt & #2>&1 </dev/null &

#gosu postgres psql --command "CREATE USER root WITH CREATEDB CREATEROLE"

python3.9 -m pip install --no-cache-dir pyyaml

#timeout 3m bash -c 'until exec gosu postgres pg_isready --port=/var/run/postgresql/.s.PGSQL.5432 ; do sleep 5 ; done'
if gosu postgres pg_isready -t 240; then
    gosu postgres psql --command "CREATE USER root WITH CREATEDB CREATEROLE"
fi

python3.9 -u -m testing.downstream_testing.downstream_runner $INPUT_DS_NAME $INPUT_DS_YAML $INPUT_DS_JOBS --matrix-exclude $INPUT_DS_MATRIX_EXCLUDE

#gosu postgres cat /var/log/postgresql/log.txt