FROM golang:1.18-buster as builder

RUN apt-get update && \
    apt-get install -y \
        git \
        curl \
        make \
        liblzo2-dev \
        libbrotli-dev \
        python3 \
        python3-pip && \
        mkdir -p /opt/cmd/build_walg /opt/utils/ && \
        touch /opt/cmd/__init__.py /opt/utils/__init__.py

WORKDIR /opt

COPY src/cmd/build_walg /opt/cmd/build_walg
COPY src/utils/commands.py /opt/utils/commands.py

ARG WALG_COMMIT
ARG WALG_REPO
ENV PYTHONUNBUFFERED=1

RUN python3 -m cmd.build_walg.main --commit $WALG_COMMIT --repo $WALG_REPO

###################################################

FROM python:3.9.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests \
    libbrotli-dev \
    time \
    postgresql \
    postgresql-contrib && \
    chmod 777 /opt

COPY --from=builder /wal-g /usr/local/bin/wal-g
COPY --from=builder /tmp/build-info.json /build-info.json

USER postgres

WORKDIR /opt

COPY src/requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY src bench.yaml ./

COPY static static

USER root

RUN chmod -R 777 ./static

USER postgres

ENV PYTHONUNBUFFERED=1
ENV PGDATA=/var/lib/postgresql/data

ENTRYPOINT ["python3", "-m", "cmd.client.main"]
