from abc import ABC, abstractmethod
from typing import List

from internal.base.result import Result


class BaseBenchmark(ABC):
    def prepare(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def results(self) -> List[Result]:
        pass
