
import datetime

from typing import Any

from services.modules.datetime_processing import make_datetime_object
from services.modules.weather_info import WeatherInformation


class StandardParser:
    """
        Класс StandardParser реализует парсинг данных о погоде.

    """

    @staticmethod
    def parsing_weather_data(weather_data: dict[str, Any]) -> WeatherInformation:
        """
            Эта функция парсит данные и переводит их в нужный формат

            Args:
                (weather_data: Any): информация о погоде от api запроса
            Returns:
                WeatherInformation: преобразованная информация о погоде в виде класса
        """
        request_time = weather_data['dt']
        offset_from_utc = weather_data['timezone']
        date_request = make_datetime_object(request_time, offset_from_utc)
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
