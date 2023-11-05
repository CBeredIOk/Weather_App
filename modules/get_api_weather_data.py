
import geocoder
import requests
from http import HTTPStatus

from files import settings
from files import interface_text
from .app_errors import error_handler
from .process_weather_data import processing_weather_data
from .app_errors import (ApiRequestError, MissCityError, LostConnectionError)


def get_weather_data_in_my_location() -> None:
    """
    Эта функция получает название города в местоположении пользователя и отправляет в функцию API запроса.

    Returns:
        None
    """
    get_api_request(get_current_city())


def get_weather_data_in_city() -> None:
    """
    Эта функция получает название города от пользователя и отправляет в функцию API запроса.

    Returns:
        None
    """
    city_name = input(interface_text.ENTER_CITY).strip()
    get_api_request(city_name)


@error_handler
def get_api_request(location: str) -> None:
    """
    Эта функция отправляет http запрос и отправляет полученную информацию на обработку.

    Args:
        (location: Optional[str]): Название города, по которому будет отправлен http запрос.
    Returns:
        None
    """
    api_url = settings.API_GET_REQUEST_CITY_WEATHER.format(location=location, api_key=settings.API_KEY)
    response = requests.get(api_url)
    try:
        response.raise_for_status()
        data = response.json()
        processing_weather_data(data)
    except requests.exceptions.HTTPError:
        if (
            response.status_code == HTTPStatus.NOT_FOUND or
            response.status_code == HTTPStatus.BAD_REQUEST
        ):
            raise MissCityError
        elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ApiRequestError
    except requests.exceptions.ConnectionError:
        raise LostConnectionError


def get_current_city() -> str:
    """
    Эта функция возвращает название города по текущему местоположению пользователя.

    Returns:
        str: название города
    """
    return geocoder.ip('me').city
