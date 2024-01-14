
from typing import Any, Protocol

from services.modules.weather_info import WeatherInformation


class Parser(Protocol):

    @staticmethod
    def parsing_weather_data_from_request(weather_data: dict[str, Any]) -> WeatherInformation:
        raise NotImplementedError

    @staticmethod
    def formoting_data_from_storage(weather_data: dict[str, Any]) -> WeatherInformation:
        raise NotImplementedError
