
import datetime
from typing import Any

from .app_errors import error_handler
from .storage_weather_data import remembering_data_weather

from services.app_classes.weather_info import WeatherInformation


def processing_weather_data(weather_data: Any) -> WeatherInformation:
    """
    Эта функция обрабатывает полученную информацию

    Функция отправляет данные на парсинг,
    потом создаёт объект класса WeatherInformation на основе полученных данных,
    отправляет информацию на сохранение и производит её вывод.

    Args:
        (weather_data: Any): Словарь с информацией о погоде в городе.
    Returns:
        WeatherInformation: преобразованная информация о погоде в виде класса
    """
    processed_weather_data = parse_weather_data(weather_data)
    remembering_data_weather(processed_weather_data)
    return processed_weather_data


def parse_weather_data(weather_data: Any) -> WeatherInformation:
    """
    Эта функция парсит данные и переводит их в нужный формат

    Args:
        (weather_data: Any): информация о погоде от api запроса
    Returns:
        WeatherInformation: преобразованная информация о погоде в виде класса
    """
    date_request = make_datetime_object(weather_data["dt"], weather_data["timezone"])
    weather_parsing_data = {
        'date': date_request,
        'city_name': weather_data['name'],
        'weather_conditions': weather_data['weather'][0]['description'],
        'temperature': int(weather_data['main']['temp']),
        'temperature_feels_like': int(weather_data['main']['feels_like']),
        'wind_speed': int(weather_data['wind']['speed'])
    }
    weather_information = WeatherInformation(**weather_parsing_data)
    return weather_information


@error_handler
def make_datetime_object(request_time: str, offset_from_utc: str) -> datetime.datetime:
    """
    Эта функция переводит время из timestep в формат datetime и показывает разницу по UTC

    Args:
        (request_time: str): время в городе при запросе
        (offset_from_utc: str): показывает разницу времени в городе от utc
    Returns:
        datetime: дата и время в городе при http запросе
    """
    timezone = datetime.timezone(datetime.timedelta(seconds=float(offset_from_utc)))
    return datetime.datetime.fromtimestamp(float(request_time), timezone)
