ARG ACTION_IMAGE=python:3.8

FROM $ACTION_IMAGE

COPY entrypoint.sh /entrypoint.sh
#COPY downstream_runner.py /downstream_runner.py

RUN apt-get update && \
    apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev\
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev && \
    curl https://pyenv.run | bash


RUN pip install --no-cache-dir pyyaml

#CMD [ "python", "-m", "downstream_runner", $DS_YAML, $DS_JOBS, $DS_EXCLUDE]

ENTRYPOINT [ "/entrypoint.sh" ]
