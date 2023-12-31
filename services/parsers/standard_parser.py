import datetime
from typing import Any

from services.modules.weather_info import WeatherInformation


class StandardParser:
    @staticmethod
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

    def parsing_weather_data(self, weather_data: dict[str, Any]) -> WeatherInformation:
        """
        Эта функция парсит данные и переводит их в нужный формат

        Args:
            (weather_data: Any): информация о погоде от api запроса
        Returns:
            WeatherInformation: преобразованная информация о погоде в виде класса
        """
        date_request = self.make_datetime_object(weather_data["dt"], weather_data["timezone"])
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
