import logging

from minio import Minio

from utils.const import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_ENDPOINT
from utils.exceptions.minio import MinioBucketDoesntExist


def new_client():
    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )


def minio_delete_object(bucket: str, bucket_path: str) -> bool:
    logging.info(f'deleting {bucket}/{bucket_path} from minio')

    client = new_client()
    if minio_object_exist(bucket, bucket_path):
        client.remove_object(bucket, bucket_path)
        return True

    return False


def minio_object_exist(bucket: str, bucket_path: str) -> bool:
    client = new_client()
    if not client.bucket_exists(bucket):
        return False

    names = {obj.object_name for obj in client.list_objects(bucket, bucket_path)}
    return bucket_path in names


def upload_to_bucket(os_path: str, bucket: str, bucket_path: str, bucket_create: bool = False) -> None:
    logging.info(f'trying to upload {os_path} to minio bucket {bucket} with path {bucket_path}')
    client = new_client()

    found = client.bucket_exists(bucket)
    if not found:
        if not bucket_create:
            logging.error('minio bucket doesnt exist and bucket_create=False')
            raise MinioBucketDoesntExist(bucket)

        client.make_bucket(bucket)

    client.fput_object(
        bucket_name=bucket,
        object_name=bucket_path,
        file_path=os_path,
    )

    logging.info(f'upload {os_path} to minio succeed!')
