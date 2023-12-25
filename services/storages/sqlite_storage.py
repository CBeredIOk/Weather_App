import datetime
import sqlite3

from services.app_classes.weather_info import WeatherInformation
from services.files.db_settings import (
    SELECT_N_LAST_REQUEST, NAME_TABLE, INSERT_REQUEST_INTO_TABLE,
    DELETE_FROM_REQUEST, CREATE_DATABASE_REQUEST, NAME_DATABASE, REFRESH_ID
)
from services.modules.app_errors import DatabaseException
from services.storages.contracts import Storage


class SQLiteStorage(Storage):
    def create_db_weather(self) -> None:
        """
        Функция создает базу данных, если она еще не создана в каталоге.

        Returns:
            None
        """
        cursor = self.connection.cursor()
        cursor.execute(CREATE_DATABASE_REQUEST.format(NAME_TABLE))

    def __init__(self) -> None:
        self.connection = sqlite3.connect(NAME_DATABASE)
        self.create_db_weather()

    def save_data_weather(self, weather_data: WeatherInformation) -> None:
        """
        Функция получает объект погоды и извлекает из него необходимые данные для сохранения.

        Args:
            weather_data(WeatherInformation): объект Погоды, который содержит данные для вывода.

        Returns:
            None

        Raise:
            DatabaseException - райсит, если случается ошибка при работе с БД
        """
        try:
            connection = sqlite3.connect(NAME_DATABASE)
            cursor = connection.cursor()

            query = INSERT_REQUEST_INTO_TABLE.format(NAME_TABLE)

            formatted_date = str(weather_data.date)

            params = (None, formatted_date, weather_data.city_name, weather_data.weather_conditions,
                      weather_data.temperature, weather_data.temperature_feels_like, weather_data.wind_speed)

            cursor.execute(query, params)
            connection.commit()

            cursor.close()
            connection.close()
        except Exception:
            raise DatabaseException()

    def get_last_n_request(self, count_of_records: int) -> dict[int, WeatherInformation]:
        """
        Функция получает данные из Базы Данных в количестве {count_records_output} последних штук.
        Если данных меньше, чем {count_records_output}, то вернутся просто все имеющиееся данные.

        Args:
            count_of_records(int): количество строк, необходимое для просмотра пользователю

        Returns:
            list[WeatherReading] - возвращает список Объектов Погоды, готовые для вывода пользователю.

        Raises:
            DatabaseException: на случай ошибок во время работы с Базой Данных.
        """

        try:
            connection = sqlite3.connect(NAME_DATABASE)
            cursor = connection.cursor()

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
            connection.close()

            return weather_data_dict
        except Exception:
            raise DatabaseException()

    def delete_request_history(self) -> None:
        """
        Функция очищает таблицы с данными.

        Returns:
            None

        Raise:
            DatabaseException - райзит, когда возникают проблемы с БД
        """
        try:
            connection = sqlite3.connect(NAME_DATABASE)
            cursor = connection.cursor()

            cursor.execute(DELETE_FROM_REQUEST.format(NAME_TABLE,))
            cursor.execute(REFRESH_ID)
            connection.commit()

            cursor.close()
            connection.close()
        except Exception:
            raise DatabaseException()
