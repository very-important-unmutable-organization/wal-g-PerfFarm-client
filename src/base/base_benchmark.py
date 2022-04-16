from abc import ABC, abstractmethod
from typing import List

from base.result import Result


class BaseBenchmark(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def results(self) -> List[Result]:
        pass
