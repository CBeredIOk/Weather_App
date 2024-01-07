
import requests

from services.files import settings
from services.weather_searchers.contracts import WeatherSearcher
from services.modules.raising_errors import LostConnectionError, error_handler, raising_http_errors


class OpenWeatherAPISearcher(WeatherSearcher):
    @error_handler
    def get_weather(self, location: str) -> dict[str, str]:
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
            raising_http_errors(response.status_code)
        except requests.exceptions.ConnectionError:
            raise LostConnectionError
