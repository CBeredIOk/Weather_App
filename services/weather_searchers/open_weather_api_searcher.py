
import requests

from http import HTTPStatus

from services.files import settings
from services.weather_searchers.contracts import WeatherSearcher
from services.modules.app_errors import MissCityError, ApiRequestError, LostConnectionError, error_handler


class OpenWeatherAPISearcher(WeatherSearcher):
    @staticmethod
    def raising_http_errors(status_code: int) -> None:
        """
        Проверяет код состояния HTTP и возбуждает соответствующие ошибки.

        Args:
            status_code (int): Код состояния HTTP.
        Returns:
            None
        """

        if status_code == HTTPStatus.NOT_FOUND or status_code == HTTPStatus.BAD_REQUEST:
            raise MissCityError
        elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ApiRequestError

    @error_handler
    def get_weather(self, location: str) -> dict[str: str]:
        """
        Отправляет HTTP-запрос для получения информации о погоде по указанному местоположению.

        Args:
            location (str): Название города, по которому будет отправлен HTTP-запрос.
        Returns:
            dict[str, str]: Информация о погоде в виде словаря.
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
