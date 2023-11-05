
import datetime
from typing import Any

from app_classes.weather_info_class import WeatherInformation
from .storage_weather_data import remembering_data_weather


def processing_weather_data(weather_data: dict[str, str]) -> None:
    """
    Эта функция обрабатывает полученную информацию

    Функция отправляет данные на парсинг,
    потом создаёт объект класса WeatherInformation на основе полученных данных,
    отправляет информацию на сохранение и производит её вывод.

    Args:
        (weather_data: dict[str, str]): Словарь с информацией о погоде в городе.
    Returns:
        None
    """
    weather_data_with_parsing = parse_weather_data(weather_data)
    weather_data_class = WeatherInformation(**weather_data_with_parsing)
    remembering_data_weather(weather_data_class)
    print(weather_data_class)


def parse_weather_data(weather_data: Any) -> dict[str, Any]:
    """
    Эта функция парсит данные и переводит их в нужный формат

    Args:
        (weather_data: Any): информация о погоде от api запроса
    Returns:
        dict[str, Any]: преобразованная информация в виде словаря
    """
    weather_data_dict = {
        'date': make_datetime_object(weather_data["dt"], weather_data["timezone"]),
        'city_name': weather_data['name'],
        'weather_conditions': weather_data['weather'][0]['description'],
        'temperature': int(weather_data['main']['temp']),
        'temperature_feels_like': int(weather_data['main']['feels_like']),
        'wind_speed': int(weather_data['wind']['speed'])
    }
    return weather_data_dict


def make_datetime_object(request_time: str, timedelta_seconds: str) -> datetime.datetime:
    """
    Эта функция переводит время из timestep в формат datetime и показывает разницу по UTC

    Args:
        (request_time: str): время в городе при запросе
        (timedelta_seconds: str): показывает разницу времени в городе от 0 часового пояса
    Returns:
        datetime: дата и время в городе при http запросе
    """
    timezone = datetime.timezone(datetime.timedelta(seconds=float(timedelta_seconds)))
    return datetime.datetime.fromtimestamp(float(request_time), timezone)
