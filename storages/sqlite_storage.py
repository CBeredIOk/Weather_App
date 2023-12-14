
from services.storages.contracts import Storage
from services.app_classes.weather_info import WeatherInformation


class SQLiteStorage(Storage):

    def __init__(self) -> None:
        pass

    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        pass

    def get_last_n_request(self, count_of_records: int) -> dict[int, WeatherInformation]:
        pass

    def delete_request_history(self) -> None:
        pass
