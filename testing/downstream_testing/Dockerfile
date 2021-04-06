FROM python:latest

COPY entrypoint.sh /entrypoint.sh
COPY postgres_entrypoint.sh ./
COPY pyenv-versions.txt ./

RUN apt-get update
RUN apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ENV LC=en_US.UTF-8


#### PostgreSQL ####
# explicitly set user/group IDs
RUN set -eux; \
	groupadd -r postgres --gid=999; \
# https://salsa.debian.org/postgresql/postgresql-common/blob/997d842ee744687d99a2b2d95c1083a2615c79e8/debian/postgresql-common.postinst#L32-35
	useradd -r -g postgres --uid=999 --home-dir=/var/lib/postgresql --shell=/bin/bash postgres; \
# also create the postgres user's home directory with appropriate permissions
# see https://github.com/docker-library/postgres/issues/274
	mkdir -p /var/lib/postgresql; \
	chown -R postgres:postgres /var/lib/postgresql

RUN apt-get -y --no-install-recommends install postgresql postgresql-client libpq-dev

# grab gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
ENV GOSU_VERSION 1.12
RUN set -eux; \
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends ca-certificates wget; \
	rm -rf /var/lib/apt/lists/*; \
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	gpgconf --kill all; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	chmod +x /usr/local/bin/gosu; \
	gosu --version; \
	gosu nobody true

RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod 2777 /var/run/postgresql
RUN mkdir /docker-entrypoint-initdb.d
ENV PATH $PATH:/usr/lib/postgresql/11/bin
ENV PGDATA /var/lib/postgresql/data
# this 777 will be replaced by 700 at runtime (allows semi-arbitrary "--user" values)
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 777 "$PGDATA"
VOLUME /var/lib/postgresql/data
ENV POSTGRES_USER=root
ENV POSTGRES_HOST_AUTH_METHOD=trust
USER postgres
#RUN echo "host all all  0.0.0.0/0 md5" >> /var/lib/postgresql/11/main/pg_hba.conf
#RUN echo "listen_addresses='*'\nunix_socket_directories = '/var/run/postgresql'" >> /var/lib/postgresql/11/main/postgresql.conf
#RUN cat /var/lib/postgresql/11/main/postgresql.conf
#RUN ls -l /usr/lib/postgresql/11/bin
#RUN /etc/init.d/postgresql start && \
#    psql --command "CREATE USER root WITH CREATEDB CREATEROLE"
#VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER root
EXPOSE 5432

#### MySQL ####


#### pyenv ####
ENV PYENV_ROOT /root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN curl https://pyenv.run | bash
#RUN xargs -a pyenv-versions.txt -P 4 -n 1 pyenv install \
#    && xargs -a pyenv-versions.txt pyenv global

ENTRYPOINT [ "/entrypoint.sh" ]

#CMD ["postgres"]