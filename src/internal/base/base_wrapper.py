from abc import ABC, abstractmethod

from internal.base.base_benchmark import BaseBenchmark


class BaseWrapper(ABC):
    @abstractmethod
    def prepare(self, bench: BaseBenchmark):
        pass

    @abstractmethod
    def cleanup(self, bench: BaseBenchmark):
        pass
