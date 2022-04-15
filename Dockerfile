FROM golang:1.18-buster as builder

RUN apt update && \
    apt install -y \
        curl \
        git \
        make \
        liblzo2-dev \
        libbrotli-dev \
        python3 \
        python3-pip

WORKDIR /opt

COPY build_walg .

ARG WALG_COMMIT
ENV PYTHONUNBUFFERED=1

RUN python3 /opt/main.py --commit $WALG_COMMIT

ENTRYPOINT ["/wal-g", "--version"]

###################################################

FROM python:3.9.12-slim

RUN apt update && apt install -y libbrotli-dev

COPY --from=builder /wal-g /usr/local/bin/wal-g

WORKDIR /opt

COPY src/requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY src .

ENTRYPOINT ["python3", "/opt/main.py"]
