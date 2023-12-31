from http import HTTPStatus

import requests

from services.files import settings
from services.modules.app_errors import MissCityError, ApiRequestError, LostConnectionError
from services.weather_searchers.contracts import WeatherSearcher


class OpenWeatherAPISearcher(WeatherSearcher):
    @staticmethod
    def raising_http_errors(status_code) -> None:
        if (
                status_code == HTTPStatus.NOT_FOUND or
                status_code == HTTPStatus.BAD_REQUEST
        ):
            raise MissCityError
        elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ApiRequestError

    def get_weather(self, location: str) -> dict[str: str]:
        """
        Эта функция отправляет http запрос и отправляет полученную информацию на обработку.

        Args:
            (location: str): Название города, по которому будет отправлен http запрос.
        Returns:
            WeatherInformation: преобразованная информация о погоде в виде класса
        """
        api_url = settings.API_GET_REQUEST_CITY_WEATHER.format(location=location, api_key=settings.API_KEY)
        response = requests.get(api_url)
        try:
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError:
            self.raising_http_errors(response.status_code)
        except requests.exceptions.ConnectionError:
            raise LostConnectionError
