import logging
import os
from typing import List

from internal.base.base_benchmark import BaseBenchmark
from internal.base.result import Result
from utils.exceptions.benchmarks import BenchmarkNotRanResults, BenchmarkNotConfigured, BenchmarkError
from utils.walg.run_walg_command import time_walg_command


class RunWalFetchNTimes(BaseBenchmark):
    def __init__(self, times: int):
        self.times = times
        self._results = []
        self.pushed_wal_name = None  # this field must be set by wrapper

    def run(self) -> None:
        if self.pushed_wal_name is None:
            raise BenchmarkNotConfigured(
                'benchmark doesnt now which wal archive it have to fetch.'
                ' this info must be provided by one of the wrappers in field pushed_wal_name'
            )

        total_mem, total_time_user, total_time_system = 0, 0, 0

        for i in range(self.times):
            if os.path.isfile('./archive.wal'):
                os.remove('./archive.wal')

            ret_code, out, err = time_walg_command(
                f'wal-fetch {self.pushed_wal_name} ./archive.wal',
                '%M %e %S'
            )

            if ret_code != 0:
                logging.error('non zero return code for wal-fetch command')
                logging.error(f'stdout: {out}; stderr: {err}')
                raise BenchmarkError('nonzero return code in walg run')

            time_out = err.strip('"').replace('\n', '')
            mem, user_time, system_time = time_out.split()

            total_mem += int(mem)
            total_time_user += float(user_time)
            total_time_system += float(system_time)

        self._results.append(Result('avg_mem_kb', total_mem / self.times))
        self._results.append(Result('avg_user_time_seconds', total_time_user / self.times))
        self._results.append(Result('avg_system_time_seconds', total_time_system / self.times))

    def results(self) -> List[Result]:
        if not self._results:
            raise BenchmarkNotRanResults()

        return self._results
