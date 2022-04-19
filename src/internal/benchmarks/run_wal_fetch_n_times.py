import logging
import time
from typing import List

from internal.base.base_benchmark import BaseBenchmark
from internal.base.result import Result
from utils.commands import run_command
from utils.exceptions.benchmarks import BenchmarkNotRanResults


class RunWalFetchNTimes(BaseBenchmark):
    def __init__(self, times: int):
        self.times = times
        self.results = []

    def run(self) -> None:
        total_duration = 0
        times = 0
        for i in range(self.times):
            start = time.perf_counter()
            ret_code, out, err = run_command('wal-g wal-fetch')
            duration = time.perf_counter() - start

            total_duration += duration
            times += 1
            if ret_code != 0:
                logging.error(f'stdout: {out}, stderr: {err}')

        self.results.append(Result(f'wal_fetch_avg_time_{self.times}_runs', total_duration / times))

    def results(self) -> List[Result]:
        if not self.results:
            raise BenchmarkNotRanResults()

        return self.results
