from utils.const import MINIO_POSTGRES_BACKUP_BUCKET
from utils.minio.crud import new_client


def setup_minio():
    client = new_client()
    if not client.bucket_exists(MINIO_POSTGRES_BACKUP_BUCKET):
        client.make_bucket(MINIO_POSTGRES_BACKUP_BUCKET)
