#!/bin/bash

python -m testing.downstream_testing.downstream_runner $INPUT_DS_YAML $INPUT_DS_JOBS --matrix-exclude $INPUT_DS_EXCLUDE