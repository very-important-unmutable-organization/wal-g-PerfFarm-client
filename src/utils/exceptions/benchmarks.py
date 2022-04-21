from utils.exceptions.base import WalgPerformanceFarmBase


class BenchmarkError(WalgPerformanceFarmBase):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return self.reason


class BenchmarkNotRanResults(BenchmarkError):
    def __init__(self):
        super().__init__('benchmark results method called before benchmark run')


class BenchmarkNotConfigured(BenchmarkError):
    pass
