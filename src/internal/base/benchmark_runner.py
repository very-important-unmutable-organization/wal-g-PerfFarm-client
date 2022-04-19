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
        self.prepare()
        self.run_bench()
        self.cleanup()

        runner_results = []
        for bench_result in self.bench.results():
            runner_result_name = f'{self.name}_{bench_result.metric_name}'
            runner_results.append(
                Result(runner_result_name, bench_result.metric_value)
            )

        return runner_results

    def prepare(self) -> None:
        for wrapper in self.wrappers:
            wrapper.prepare(self.bench)

    def cleanup(self) -> None:
        for wrapper in reversed(self.wrappers):
            wrapper.cleanup(self.bench)

    def run_bench(self) -> None:
        self.bench.prepare()
        self.bench.run()
        self.bench.cleanup()
