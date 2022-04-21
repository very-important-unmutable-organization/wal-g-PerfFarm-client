import logging
import os
import random
from random import randbytes
from tempfile import TemporaryDirectory

from internal.base.base_benchmark import BaseBenchmark
from internal.base.base_wrapper import BaseWrapper
from utils.const import MINIO_POSTGRES_BACKUP_BUCKET
from utils.minio.crud import minio_delete_object
from utils.walg.run_walg_command import run_walg_command

KB = 1024
MB = 1024 * KB
WAL_SIZE = 16 * MB


def generate_correct_wal_name() -> str:
    wal_segment_size = 16 * 1024 * 1024
    x_log_segments_per_x_log_id = 0x100000000 // wal_segment_size

    first_part = random.randbytes(8).hex()
    second_part = random.randint(0, x_log_segments_per_x_log_id - 1).to_bytes(4, 'big').hex()

    return (first_part + second_part).upper()


class RandomWalGenerator(BaseWrapper):
    def __init__(self):
        self.bucket = MINIO_POSTGRES_BACKUP_BUCKET
        self.name = None

    def prepare(self, bench: BaseBenchmark):
        logging.debug('generating random bytes for walg')
        with TemporaryDirectory() as tempdir:
            wal_name = generate_correct_wal_name()
            wal_path = os.path.join(tempdir, wal_name)
            self.name = f'/wal_005/{wal_name}'

            chunk_size = MB
            needed_size = WAL_SIZE
            with open(wal_path, 'wb') as f:
                while needed_size != 0:
                    write_size = min(needed_size, chunk_size)
                    needed_size -= write_size
                    f.write(randbytes(write_size))
                run_walg_command(f'wal-push {wal_path}')

            bench.pushed_wal_name = wal_name

    def cleanup(self, bench: BaseBenchmark):
        logging.debug('cleanup for random walg wrapper')
        minio_delete_object(self.bucket, self.name)
