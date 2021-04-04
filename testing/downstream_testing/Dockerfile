ARG ACTION_IMAGE=python:latest

FROM $ACTION_IMAGE

COPY entrypoint.sh /entrypoint.sh
COPY pyenv-versions.txt ./
#COPY downstream_runner.py /downstream_runner.py

RUN apt-get update
RUN apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

RUN apt-get -y install postgresql postgresql-client libpq-dev
#RUN /etc/init.d/postgresql start
#RUN pg_isready
#RUN psql --command "CREATE USER root" && createdb -O root

ENV PYENV_ROOT /root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN curl https://pyenv.run | bash

RUN xargs -a pyenv-versions.txt -P 4 -n 1 pyenv install \
    && xargs -a pyenv-versions.txt pyenv global

ENTRYPOINT [ "/entrypoint.sh" ]
