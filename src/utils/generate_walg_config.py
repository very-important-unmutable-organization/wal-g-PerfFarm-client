import json

from utils.const import MINIO_POSTGRES_BACKUP_BUCKET, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_ENDPOINT, \
    WALG_CONFIG_PATH


def generate_walg_config():
    config = {
        "WALG_S3_PREFIX": f"s3://{MINIO_POSTGRES_BACKUP_BUCKET}/",
        "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_KEY,
        "AWS_ENDPOINT": f"http://{MINIO_ENDPOINT}",
        "AWS_S3_FORCE_PATH_STYLE": True,
        "WALG_DOWNLOAD_CONCURRENCY": 1,
        "WALG_UPLOAD_CONCURRENCY": 1,
        "PGHOST": "localhost",
        "PGPORT": 5432,
        "PGUSER": "postgres",
        "PGSSLMODE": "disable"
    }

    with open(WALG_CONFIG_PATH, 'w') as f:
        f.write(json.dumps(config))
