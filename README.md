# WAL-G performance farm client
client for running wal-g benchmarks and sending results to server.

# Running
```bash
./client.sh ${WALG_COMMIT} ${WALG_REPO}
```

This builds Docker image with WAL-G, then runs benchmarks specified in bench.yaml
