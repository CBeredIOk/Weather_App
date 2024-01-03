
import os
import json
import datetime

from typing import Any

from services.files import settings
from services.storages.contracts import Storage
from services.modules.weather_info import WeatherInformation
from services.modules.app_errors import error_handler, OpenStorageError, SaveStorageError


class JsonStorage(Storage):
    """
        Класс JsonStorage реализует хранение данных о погоде в формате JSON.

        Этот класс позволяет сохранять информацию о погоде в файл JSON, читать сохраненные данные,
        удалять историю запросов погоды и получать последние запросы погоды.

        Attributes:
            file_path (str): Путь к файлу JSON.
    """

    def __init__(self):
        self.file_path = self.find_storage_path()

    def __enter__(self):
        self.file = open(self.file_path, 'r+')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

    @staticmethod
    def find_storage_path() -> str:
        """
            Находит путь к файлу json.

            Returns:
                str: Путь к файлу в виде строки.
        """
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)

        json_file_path = os.path.join(parent_dir, settings.STORAGE_FOLDER, settings.STORAGE_FILE_NAME)
        return json_file_path

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
            json.dump(data, self.file, indent=4, default=self.datetime_serializer)
            self.file.truncate()
        except (TypeError, ValueError):
            raise SaveStorageError

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
            return self.get_last_n_request_from_storage(n, all_weather_data)
        else:
            return self.get_last_n_request_from_storage(number_of_records, all_weather_data)

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

    @staticmethod
    def formoting_data_from_dict(weather_data: dict[str, Any]) -> WeatherInformation:
        """
            Формирует объект WeatherInformation из словаря данных о погоде.

            Args:
                weather_data (dict[str, Any]): Данные о погоде в виде словаря.
            Returns:
                WeatherInformation: Объект с информацией о погоде.
        """

        date_time = weather_data['date']
        date_time_obj = datetime.datetime.fromisoformat(date_time)

        weather_info = WeatherInformation(
            date=date_time_obj,
            city_name=weather_data['city_name'],
            weather_conditions=weather_data['weather_conditions'],
            temperature=int(weather_data['temperature']),
            temperature_feels_like=int(weather_data['temperature_feels_like']),
            wind_speed=int(weather_data['wind_speed'])
        )
        return weather_info

    def get_last_n_request_from_storage(
            self, n: int,
            all_weather_data: dict[str, Any]
    ) -> dict[int, WeatherInformation]:
        """
            Возвращает последние n запросов погоды из общих данных.

            Args:
                n (int): Количество последних запросов погоды для получения.
                all_weather_data (dict[str, Any]): Все данные о погоде.
            Returns:
                dict[int, WeatherInformation]: Словарь с последними запросами погоды.
        """

        number_of_records = len(all_weather_data)
        n_last_data = {}
        for number_of_record in range(number_of_records, number_of_records - n, -1):
            weather_data = self.formoting_data_from_dict(all_weather_data[str(number_of_record)])
            n_last_data[int(number_of_record)] = weather_data
        return n_last_data

    def delete_request_history(self) -> None:
        """
            Удаляет историю запросов погоды.

            Returns:
                None
        """

        empty_dictionary = {}
        self.write_new_data_to_json(empty_dictionary)

    @staticmethod
    def datetime_serializer(date: datetime.datetime) -> str:
        """
            Сериализует объект даты и времени в строку.

            Args:
                date (datetime.datetime): Объект даты и времени.
            Returns:
                str: Сериализованная строка с датой и временем.
        """

        if isinstance(date, datetime.datetime):
            return date.strftime(settings.DATA_TYPE_PRINT)
        raise TypeError
