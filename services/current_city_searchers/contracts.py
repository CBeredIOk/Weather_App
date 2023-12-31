
from typing import Protocol


class CurrentCitySearcher(Protocol):
    @staticmethod
    def get_current_city() -> str:
        raise NotImplementedError
