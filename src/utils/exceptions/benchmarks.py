from utils.exceptions.base import WalgPerformanceFarmBase


class BenchmarkNotRanResults(WalgPerformanceFarmBase):
    def __str__(self):
        return 'benchmark results method called before benchmark run'
