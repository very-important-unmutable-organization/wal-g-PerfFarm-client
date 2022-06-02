import logging

from internal.base.base_benchmark import BaseBenchmark
from internal.base.base_wrapper import BaseWrapper
from utils.commands import run_command_out_to_shell
from utils.const import MINIO_POSTGRES_BACKUP_BUCKET
from utils.minio.crud import minio_delete_object
from utils.walg.run_walg_command import run_walg_command, run_walg_command_out_to_shell


class PGWalPusher(BaseWrapper):
    def __init__(self):
        self.bucket = MINIO_POSTGRES_BACKUP_BUCKET
        self.wal_name = '000000010000000000000002'

    def prepare(self, bench: BaseBenchmark):
        logging.debug('pushing prepared wal from static dir')

        ret_code, _, _ = run_walg_command(f'wal-push ./static/real_wal/{self.wal_name}')
        if ret_code != 0:
            raise RuntimeError("wal-push command returned non zero code")

        bench.pushed_wal_name = self.wal_name

    def cleanup(self, bench: BaseBenchmark):
        minio_delete_object(self.bucket, f'/wal_005/{self.wal_name}')
