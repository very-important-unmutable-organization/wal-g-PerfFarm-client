# WAL-G performance farm client
client for running wal-g benchmarks and sending results to server.

# Building
```bash
./client.sh ${WALG_COMMIT} ${WALG_REPO}
```

This builds Docker image with WAL-G

---

# Running

At this moment client doesn't run any tests,
it only builds docker image with wal-g.
Very soon there will be a real client, that will use image with
built wal-g as a base.
