FROM debian:8.10-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG NAME=exitnode
ARG DIR=/$NAME

# install gosu

RUN apt-get update && apt-get -y --no-install-recommends install \
    ca-certificates \
    curl \
    sudo

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

# deps

COPY ./build/bin/install-dependencies /tmp/install-dependencies
RUN apt-get update && /tmp/install-dependencies

# workdir

RUN mkdir -p $DIR
WORKDIR $DIR
COPY . $DIR
ENV EXITNODE_DIR=$DIR

ARG PUBLIC_IP=REPLACE.ME.WITH.EXITNODE.PUBLIC.IP

RUN ./build/docker/docker-build

ENTRYPOINT ["./build/docker-entrypoint.sh"]

CMD ./build/docker/docker-cmd
