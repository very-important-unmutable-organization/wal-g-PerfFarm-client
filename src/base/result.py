from typing import Dict


class Result:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def metric_name(self) -> str:
        return self.name

    @property
    def metric_value(self) -> float:
        return self.value

    def to_dict(self) -> Dict:
        return dict(
            name=self.metric_name,
            value=self.metric_value,
        )
