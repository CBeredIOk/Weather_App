
from typing import Protocol


class WeatherSearcher(Protocol):
    def get_weather(self, location: str) -> dict[str, str]:
        raise NotImplementedError
