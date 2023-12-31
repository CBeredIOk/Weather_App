
from typing import Any, Protocol

from services.modules.weather_info import WeatherInformation


class Parser(Protocol):
    def parsing_weather_data(self, weather_data: dict[str, Any]) -> WeatherInformation:
        raise NotImplementedError
