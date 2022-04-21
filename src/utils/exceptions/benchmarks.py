from utils.exceptions.base import WalgPerformanceFarmBase


class BenchmarkError(WalgPerformanceFarmBase):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return self.reason


class BenchmarkNotRanResults(BenchmarkError):
    def __init__(self):
        pass

    def __str__(self):
        return 'benchmark results method called before benchmark run'


class BenchmarkNotConfigured(BenchmarkError):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return self.reason
