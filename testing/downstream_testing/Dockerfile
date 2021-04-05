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

ENV PGDATA=/var/lib/postgresql/11/main
ENV POSTGRES_USER=root
USER postgres
RUN echo "host all all  0.0.0.0/0 md5" >> /var/lib/postgresql/11/main/pg_hba.conf
RUN echo "listen_addresses='*'\nunix_socket_directories = '/var/run/postgresql'" >> /var/lib/postgresql/11/main/postgresql.conf
RUN cat /var/lib/postgresql/11/main/postgresql.conf
RUN ls -l /usr/lib/postgresql/11/bin
#RUN /etc/init.d/postgresql start
#RUN /usr/lib/postgresql/11/bin/pg_ctl start
EXPOSE 5432
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER root WITH CREATEDB CREATEROLE"
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
CMD ["postgres"]
USER root

#### MySQL ####


#### pyenv ####
ENV PYENV_ROOT /root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN curl https://pyenv.run | bash
RUN xargs -a pyenv-versions.txt -P 4 -n 1 pyenv install \
    && xargs -a pyenv-versions.txt pyenv global

ENTRYPOINT [ "/entrypoint.sh" ]
