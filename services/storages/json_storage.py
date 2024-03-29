
import json

from typing import Any

from services.modules.datetime_processing import datetime_serializing
from services.storages.contracts import Storage
from services.modules.weather_info import WeatherInformation
from services.modules.raising_errors import error_handler, OpenStorageError, SaveStorageError


class JsonStorage(Storage):
    """
        Класс JsonStorage реализует хранение данных о погоде в формате JSON.

        Этот класс позволяет сохранять информацию о погоде в файл JSON, читать сохраненные данные,
        удалять историю запросов погоды и получать последние запросы погоды.

        Attributes:
            file_path (str): Путь к файлу JSON.
    """

    def __init__(self, **kwargs):
        self.parser = kwargs.get('parser')
        self.file_path = kwargs.get('file_name')

    def __enter__(self):
        self.file = open(self.file_path, 'r+')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

    @error_handler
    def write_new_data_to_json(self, data: dict[str, Any]) -> None:
        """
            Записывает новые данные в JSON-файл.

            Args:
                data (dict[str, Any]): Данные для записи в файл.
            Returns:
                None
        """

        try:
            self.file.seek(0)
            json.dump(data, self.file, indent=4, default=datetime_serializing)
            self.file.truncate()
        except (TypeError, ValueError):
            raise SaveStorageError

    @error_handler
    def read_all_data_from_json(self) -> Any:
        """
            Читает все данные из JSON-файла.

            Returns:
                Any: Прочитанные данные из файла.
        """

        try:
            self.file.seek(0)
            data = json.load(self.file)
            return data
        except json.JSONDecodeError:
            raise OpenStorageError

    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        """
            Сохраняет информацию о погоде в файл.

            Args:
                weather_data (WeatherInformation): Информация о погоде для сохранения.
            Returns:
                None
        """
        existing_data = self.read_all_data_from_json()
        weather_data_to_history = weather_data.to_dict()
        existing_data[str(len(existing_data) + 1)] = weather_data_to_history
        self.write_new_data_to_json(existing_data)

    def get_last_n_request(self, n: int) -> dict[int, WeatherInformation]:
        """
            Возвращает последние n запросов погоды.

            Args:
                n (int): Количество последних запросов погоды для получения.
            Returns:
                dict[int, WeatherInformation]: Словарь с последними запросами погоды.
        """

        all_weather_data = self.read_all_data_from_json()
        number_of_records = len(all_weather_data)
        if n < number_of_records:
            return self.get_last_n_request_from_json(n, all_weather_data)
        else:
            return self.get_last_n_request_from_json(number_of_records, all_weather_data)

    def get_last_n_request_from_json(
            self, n: int,
            all_weather_data: dict[str, Any]
    ) -> dict[int, WeatherInformation]:
        """
            Возвращает последние n запросов погоды из файла json.

            Args:
                n (int): Количество последних запросов погоды для получения.
                all_weather_data (dict[str, Any]): Все данные о погоде.
            Returns:
                dict[int, WeatherInformation]: Словарь с последними запросами погоды.
        """

        number_of_records = len(all_weather_data)
        n_last_data = {}
        for number_of_record in range(number_of_records, number_of_records - n, -1):
            weather_data = all_weather_data[str(number_of_record)]
            formatted_weather_data = self.parser.formoting_data_from_storage(weather_data)
            n_last_data[number_of_record] = formatted_weather_data
        return n_last_data

    def delete_request_history(self) -> None:
        """
            Удаляет историю запросов погоды.

            Returns:
                None
        """

        empty_dictionary = {}
        self.write_new_data_to_json(empty_dictionary)
