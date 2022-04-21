import logging
from typing import List

from internal.base.base_benchmark import BaseBenchmark
from internal.base.base_wrapper import BaseWrapper
from internal.base.result import Result


class BenchmarkRunner:
    def __init__(
            self,
            name: str,
            bench: BaseBenchmark,
            wrappers: List[BaseWrapper]
    ):
        self.name = name
        self.bench = bench
        self.wrappers = wrappers

    def run(self) -> List[Result]:
        logging.info(f'running {self.name} benchmark')

        self._prepare()
        self._run_bench()
        self._cleanup()

        runner_results = []
        for bench_result in self.bench.results():
            runner_result_name = f'{self.name}_{bench_result.metric_name}'
            runner_results.append(
                Result(runner_result_name, bench_result.metric_value)
            )

        logging.info(f'run of {self.name} benchmark ended')
        return runner_results

    def _prepare(self) -> None:
        for wrapper in self.wrappers:
            wrapper.prepare(self.bench)

    def _cleanup(self) -> None:
        for wrapper in reversed(self.wrappers):
            wrapper.cleanup(self.bench)

    def _run_bench(self) -> None:
        self.bench.prepare()
        self.bench.run()
        self.bench.cleanup()

    def __str__(self):
        return f'{self.name}'
