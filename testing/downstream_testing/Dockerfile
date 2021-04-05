FROM python:latest

COPY entrypoint.sh /entrypoint.sh
COPY pyenv-versions.txt ./
#COPY downstream_runner.py /downstream_runner.py

RUN apt-get update
RUN apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ENV LC=en_US.UTF-8

RUN apt-get -y install postgresql postgresql-client libpq-dev
#RUN ln -s /tmp/.s.PGSQL.5432 /var/run/postgresql/.s.PGSQL.5432
#RUN ls -l /usr/lib/postgresql/11
ENV PGDATA=/var/lib/postgresql/11/main
USER postgres
RUN echo "host all all  0.0.0.0/0 md5" >> /var/lib/postgresql/11/main/pg_hba.conf
RUN echo "listen_addresses='*'\nunix_socket_directories = '/var/run/postgresql'" >> /var/lib/postgresql/11/main/postgresql.conf
RUN cat /var/lib/postgresql/11/main/postgresql.conf
#RUN ls -l /var/lib/postgresql/11/main
#RUN /etc/init.d/postgresql start
#RUN /usr/lib/postgresql/11/bin/pg_ctl start
EXPOSE 5432
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER root WITH CREATEDB CREATEROLE"
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
USER root

ENV PYENV_ROOT /root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN curl https://pyenv.run | bash

RUN xargs -a pyenv-versions.txt -P 4 -n 1 pyenv install \
    && xargs -a pyenv-versions.txt pyenv global

ENTRYPOINT [ "/entrypoint.sh" ]
