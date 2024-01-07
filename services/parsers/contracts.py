
from typing import Any, Protocol

from services.modules.weather_info import WeatherInformation


class Parser(Protocol):

    @staticmethod
    def parsing_weather_data(weather_data: dict[str, Any]) -> WeatherInformation:
        raise NotImplementedError
