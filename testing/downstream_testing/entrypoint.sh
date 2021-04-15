#!/bin/bash

eval "$(pyenv init -)"

python3.9 -m pip install --no-cache-dir pyyaml

for VER in $(cat pyenv-versions.txt); 
do 
    pyenv shell $VER && pyenv exec pip install ./pytest; 
done

cd /pytest

python3.9 -u -m testing.downstream_testing.downstream_runner $DS_NAME $DS_YAML $DS_JOBS --matrix-exclude $DS_MATRIX_EXCLUDE
