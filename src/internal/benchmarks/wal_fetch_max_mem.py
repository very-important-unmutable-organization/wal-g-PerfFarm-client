import logging
import os
import time
from typing import List

from internal.base.base_benchmark import BaseBenchmark
from internal.base.result import Result
from utils.exceptions.benchmarks import BenchmarkNotRanResults, BenchmarkNotConfigured, BenchmarkError
from utils.walg.run_walg_command import run_walg_command


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

        total_duration = 0
        times = 0
        for i in range(self.times):
            if os.path.isfile('./random.wal'):
                os.remove('./random.wal')

            ret_code, out, err = run_walg_command(
                f'/usr/bin/time -f "%M" wal-fetch {self.pushed_wal_name} ./random.wal'
            )

            if ret_code != 0:
                logging.error('non zero return code for wal-fetch command')
                logging.error(f'stdout: {out}; stderr: {err}')
                raise BenchmarkError('nonzero return code in walg run')

            print()

        self._results.append(Result(f'avg_time', 1))

    def results(self) -> List[Result]:
        if not self._results:
            raise BenchmarkNotRanResults()

        return self._results
