
import datetime
import sqlite3

from services.modules.weather_info import WeatherInformation
from services.storages.contracts import Storage
from services.modules.custom_errors import DatabaseException

from services.files.db_params import (
    SELECT_N_LAST_REQUEST, NAME_TABLE, INSERT_REQUEST_INTO_TABLE,
    DELETE_FROM_REQUEST, CREATE_DATABASE_REQUEST, REFRESH_ID
)


class SQLiteStorage(Storage):
    """
        Класс SQLiteStorage реализует хранение данных о погоде в SQLite базе данных.

        Attributes:
            connection (sqlite3.Connection): Подключение к базе данных.
        Returns:
            None
    """

    def __init__(self, **kwargs) -> None:
        self.connection = None
        self.parser = kwargs.get('parser')
        self.name_database = kwargs.get('file_name')
        self.name_table = NAME_TABLE

    def create_db_weather(self) -> None:
        """
            Функция создает базу данных, если она еще не создана в каталоге.

            Returns:
                None
        """

        cursor = self.connection.cursor()
        cursor.execute(CREATE_DATABASE_REQUEST.format(self.name_table))

    def __enter__(self):
        self.connection = sqlite3.connect(self.name_database)
        self.create_db_weather()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        """
            Сохраняет информацию о погоде в базе данных.

            Args:
                weather_data (WeatherInformation): Информация о погоде для сохранения.
            Returns:
                None
        """

        try:
            query = INSERT_REQUEST_INTO_TABLE.format(self.name_table)
            formatted_date = str(weather_data.date)
            params = (None, formatted_date, weather_data.city_name,
                      weather_data.weather_conditions, weather_data.temperature,
                      weather_data.temperature_feels_like, weather_data.wind_speed)
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
        except Exception:
            raise DatabaseException()

    def processing_requests_data(self, rows: tuple) -> dict[int, WeatherInformation]:
        """
            Обрабатывает данные о погоде из кортежа и возвращает словарь с информацией о погоде.

            Args:
                rows (tuple): Кортеж с данными о погоде, каждая строка содержит информацию о конкретной записи.
            Returns:
                dict[int, WeatherInformation]: Словарь, где ключи - это идентификаторы записей,
                а значения - объекты WeatherInformation с информацией о погоде.
        """

        weather_data_requests = {}
        for row in rows:
            id, str_date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed = row
            datetime_date = datetime.datetime.fromisoformat(str_date)
            weather_info = WeatherInformation(
                datetime_date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed
            )
            weather_data_requests[id] = weather_info
        return weather_data_requests

    def get_last_n_request(self, count_of_records: int) -> dict[int, WeatherInformation]:
        """
            Получает последние n запросов погоды из базы данных.

            Args:
                count_of_records (int): Количество последних запросов погоды для получения.
            Returns:
                dict[int, WeatherInformation]: Словарь с последними запросами погоды.
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(SELECT_N_LAST_REQUEST.format(self.name_table, count_of_records))
            rows = cursor.fetchall()
            weather_data_requests = self.processing_requests_data(rows)
            cursor.close()
            return weather_data_requests
        except Exception:
            raise DatabaseException()

    def delete_request_history(self) -> None:
        """
            Очищает таблицу с данными в базе данных.

            Returns:
                None
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(DELETE_FROM_REQUEST.format(self.name_table))
            cursor.execute(REFRESH_ID)
            self.connection.commit()
            cursor.close()
        except Exception:
            raise DatabaseException()
