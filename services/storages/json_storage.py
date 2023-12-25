
import os
import json
import datetime
from typing import Any

from ..app_classes.weather_info import WeatherInformation
from ..modules.app_errors import error_handler
from ..modules.action_with_json import read_all_data_from_storage
from ..modules.app_errors import OpenStorageError, SaveStorageError

from services.files import settings
from services.storages.contracts import Storage


class JsonStorage(Storage):
    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        """
        Эта функция сохраняет информацию о погоде в json файл из принимаемого объекта с информацией о погоде.

        Args:
            (weather_data_to_history: dict): объект с информацией о погоде.
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
        Эта функция записывает новую информацию в файл json.

        Args:
            (data: dict[str, Any]): словарь с новой информацией для записи.
        Returns:
            None
        """
        try:
            with open(self.find_storage_path(), 'w+') as json_file:
                json.dump(data, json_file, indent=4, default=self.datetime_serializer)
        except FileNotFoundError:
            raise SaveStorageError

    def get_last_n_request(self, n: int) -> dict[int, WeatherInformation]:
        all_weather_data = read_all_data_from_storage()
        number_of_records = len(all_weather_data)
        if n < number_of_records:
            return self.n_last_request(n, all_weather_data)
        else:
            return self.n_last_request(number_of_records, all_weather_data)

    @error_handler
    def read_all_data_from_json(self) -> Any:
        """
        Эта функция считывает всю историю запросов с файла json.

        Returns:
            Any: возвращает информацию с json файла
        """
        try:
            with open(self.find_storage_path(), 'r+') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            raise OpenStorageError

    @staticmethod
    def formoting_data_from_dict(weather_data: dict[str, Any]) -> WeatherInformation:
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

    def n_last_request(self, n: int, all_weather_data: dict[str, Any]) -> dict[int, WeatherInformation]:
        """
        Эта функция выводит информацию последних n запросов.

        Args:
            (count_of_records: int): Число последних записей для вывода.
            (all_weather_data: Any): История записей
        Returns:
            None
        """
        number_of_records = len(all_weather_data)
        n_last_data = {}
        for number_of_record in range(number_of_records, number_of_records - n, -1):
            weather_data = self.formoting_data_from_dict(all_weather_data[str(number_of_record)])
            n_last_data[int(number_of_record)] = weather_data
        return n_last_data

    def delete_request_history(self) -> None:
        """
        Эта функция позволяет очищать файл с историей запросов.

        Returns:
            None
        """
        empty_dictionary = {}
        self.write_new_data_to_json(empty_dictionary)

    @staticmethod
    def find_storage_path() -> str:
        """
        Эта функция находит путь к файлу json.

        Функция поиска поднимается до Weather_App и потом переходит в папку хранения STORAGE_FOLDER

        Returns:
            str: возвращает путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)

        json_file_path = os.path.join(parent_dir, settings.STORAGE_FOLDER, settings.STORAGE_FILE_NAME)
        return json_file_path

    @staticmethod
    def datetime_serializer(date: datetime.datetime) -> str:
        """
        Сериализует объект datetime.datetime в строку с заданным форматом.

        Args:
            date (datetime.datetime): Объект datetime.datetime для сериализации.
        Returns:
            str: Строка, представляющая дату и время в указанном формате.
        """
        if isinstance(date, datetime.datetime):
            return date.strftime(settings.DATA_TYPE_PRINT)
        raise TypeError
