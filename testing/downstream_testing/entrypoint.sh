#!/bin/bash

pyenv versions

pyenv install 3.7

python -m testing.downstream_testing.downstream_runner $INPUT_DS_YAML $INPUT_DS_JOBS $INPUT_DS_EXCLUDE