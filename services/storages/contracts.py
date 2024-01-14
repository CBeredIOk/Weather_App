from typing import Protocol

from services.modules.weather_info import WeatherInformation


class Storage(Protocol):
    JsonStorage = 'JsonStorage'
    SQLiteStorage = 'SQLiteStorage'

    def save_data_weather(self, weather_info: WeatherInformation) -> None:
        raise NotImplementedError

    def get_last_n_request(self, n: int) -> dict[int, WeatherInformation]:
        raise NotImplementedError

    def delete_request_history(self) -> None:
        raise NotImplementedError
