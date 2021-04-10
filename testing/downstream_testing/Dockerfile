#FROM python:latest
FROM ubuntu:latest

COPY entrypoint.sh /entrypoint.sh
COPY pyenv-versions.txt ./

RUN apt-get update

# needed for Ubuntu to not stall on interactive tzdata setup
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get install -q -y tzdata && rm -rf /var/lib/apt/lists/*

RUN apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

RUN apt-get install -y postgresql-client mysql-client

ENV LC=en_US.UTF-8

#### pyenv ####
ENV PYENV_ROOT /root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN curl https://pyenv.run | bash
RUN xargs -a pyenv-versions.txt -P 3 -n 1 pyenv install \
    && xargs -a pyenv-versions.txt pyenv global

ENTRYPOINT [ "/entrypoint.sh" ]
