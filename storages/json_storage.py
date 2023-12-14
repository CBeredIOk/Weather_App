
from services.storages.contracts import Storage
from services.app_classes.weather_info import WeatherInformation


class JsonStorage(Storage):
    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        pass

    def get_last_n_request(self, n: int) -> dict[str, WeatherInformation]:
        pass

    def delete_request_history(self) -> None:
        pass
