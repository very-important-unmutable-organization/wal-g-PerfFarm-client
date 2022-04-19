import logging
import os
from random import randbytes
from tempfile import TemporaryDirectory

from internal.base.base_benchmark import BaseBenchmark
from internal.base.base_wrapper import BaseWrapper
from utils.const import MINIO_POSTGRES_BACKUP_BUCKET
from utils.minio.crud import upload_to_bucket, minio_object_exist, minio_delete_object

KB = 1024
MB = 1024 * KB
WAL_SIZE = 16 * MB


class RandomWalGenerator(BaseWrapper):
    def __init__(self):
        self.bucket = MINIO_POSTGRES_BACKUP_BUCKET
        self.name = 'random.wal'

    def prepare(self, bench: BaseBenchmark):
        if minio_object_exist(self.bucket, self.name):
            logging.info(f'{self.bucket}/{self.name} already exists in minio! delete.')
            return

        logging.info('generating random bytes for walg')
        with TemporaryDirectory() as tempdir, \
                open(os.path.join(tempdir, self.name), 'wb') as f:

            chunk_size = MB
            needed_size = WAL_SIZE
            while needed_size != 0:
                write_size = min(needed_size, chunk_size)
                needed_size -= write_size
                f.write(randbytes(write_size))

            upload_to_bucket(
                os.path.join(tempdir, self.name),
                MINIO_POSTGRES_BACKUP_BUCKET,
                self.name,
                bucket_create=True
            )

    def cleanup(self, bench: BaseBenchmark):
        logging.info('cleanup for random walg wrapper')
        minio_delete_object(self.bucket, self.name)
