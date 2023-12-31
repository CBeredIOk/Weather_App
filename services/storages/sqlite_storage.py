
import datetime
import sqlite3

from services.modules.weather_info import WeatherInformation
from services.storages.contracts import Storage
from services.modules.app_errors import DatabaseException

from services.files.db_params import (
    SELECT_N_LAST_REQUEST, NAME_TABLE, INSERT_REQUEST_INTO_TABLE,
    DELETE_FROM_REQUEST, CREATE_DATABASE_REQUEST, NAME_DATABASE, REFRESH_ID
)


class SQLiteStorage(Storage):
    """
        Класс SQLiteStorage реализует хранение данных о погоде в SQLite базе данных.

        Attributes:
            connection (sqlite3.Connection): Подключение к базе данных.
        Returns:
            None
    """

    def __init__(self) -> None:
        self.connection = None

    def create_db_weather(self) -> None:
        """
            Функция создает базу данных, если она еще не создана в каталоге.

            Returns:
                None
        """

        cursor = self.connection.cursor()
        cursor.execute(CREATE_DATABASE_REQUEST.format(NAME_TABLE))

    def __enter__(self):
        self.connection = sqlite3.connect(NAME_DATABASE)
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
            query = INSERT_REQUEST_INTO_TABLE.format(NAME_TABLE)
            formatted_date = str(weather_data.date)
            params = (None, formatted_date, weather_data.city_name, weather_data.weather_conditions,
                      weather_data.temperature, weather_data.temperature_feels_like, weather_data.wind_speed)

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
        except Exception:
            raise DatabaseException()

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
            cursor.execute(SELECT_N_LAST_REQUEST.format(NAME_TABLE, count_of_records))
            rows = cursor.fetchall()
            weather_data_dict = {}

            for row in rows:
                id, str_date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed = row
                datetime_date = datetime.datetime.fromisoformat(str_date)

                weather_info = WeatherInformation(
                    datetime_date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed
                )
                weather_data_dict[id] = weather_info

            cursor.close()
            return weather_data_dict
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
            cursor.execute(DELETE_FROM_REQUEST.format(NAME_TABLE,))
            cursor.execute(REFRESH_ID)
            self.connection.commit()
            cursor.close()
        except Exception:
            raise DatabaseException()
