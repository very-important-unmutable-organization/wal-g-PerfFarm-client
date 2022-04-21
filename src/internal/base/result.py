from typing import Dict


class Result:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def metric_name(self) -> str:
        return self._name

    @property
    def metric_value(self) -> float:
        return self._value

    def to_dict(self) -> Dict:
        return dict(
            name=self.metric_name,
            value=self.metric_value,
        )

    def __str__(self):
        return f'{self._name} : {self._value}'
