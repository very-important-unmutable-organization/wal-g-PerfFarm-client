#!/bin/sh

COMMIT=$1

usage() {
    echo "client for wal-g performance farm

USAGE: $0 COMMIT"
}

if [ -n "${COMMIT}" ]; then
    docker-compose build --build-arg WALG_COMMIT="${COMMIT}"
    docker-compose up --force-recreate
else
  usage
fi
