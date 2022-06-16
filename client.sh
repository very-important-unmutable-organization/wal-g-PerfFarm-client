#!/bin/sh

COMMIT=$1
REPO=$2

if [ -z "${REPO}" ]; then
  REPO="https://github.com/wal-g/wal-g"
fi

usage() {
    echo "client for wal-g performance farm

USAGE: $0 COMMIT [REPO]"
}

if [ -n "${COMMIT}" ]; then
    docker-compose build --build-arg WALG_COMMIT="${COMMIT}" --build-arg WALG_REPO="${REPO}"
    docker-compose up --force-recreate
else
  usage
fi
