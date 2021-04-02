ARG ACTION_IMAGE=python:3.8

FROM $ACTION_IMAGE

COPY entrypoint.sh /entrypoint.sh
#COPY downstream_runner.py /downstream_runner.py

RUN pip install --no-cache-dir pyyaml

#CMD [ "python", "-m", "downstream_runner", $DS_YAML, $DS_JOBS, $DS_EXCLUDE]

ENTRYPOINT [ "/entrypoint.sh" ]
