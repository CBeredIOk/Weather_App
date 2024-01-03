
from services.modules.app_errors import main_menu_error_handler

from services.weather_searchers.contracts import WeatherSearcher
from services.weather_searchers.open_weather_api_searcher import OpenWeatherAPISearcher

from services.current_city_searchers.contracts import CurrentCitySearcher
from services.current_city_searchers.geocoder_searcher import GeocoderSearcher
from services.current_city_searchers.ip_info_searcher import IpInfoSearcher

from services.storages.contracts import Storage
from services.storages.json_storage import JsonStorage
from services.storages.sqlite_storage import SQLiteStorage

from services.parsers.contracts import Parser
from services.parsers.standard_parser import StandardParser

from services.modules.weather_app import WeatherApp


def get_weather_searcher(name: str) -> WeatherSearcher:
    """
        Получает экземпляр объекта WeatherSearcher по имени.

        Args:
            name (str): Название сервиса, для получения информации о погоде.
        Returns:
            WeatherSearcher: Экземпляр объекта WeatherSearcher.
    """

    searcher_by_name = {
        'open_weather_api': OpenWeatherAPISearcher,
    }
    return searcher_by_name.get(name)()


def get_current_city_searcher(name: str) -> CurrentCitySearcher:
    """
        Получает экземпляр объекта CurrentCitySearcher по имени.

        Args:
            name (str): Название провайдера информации о текущем городе.
        Returns:
            CurrentCitySearcher: Экземпляр объекта CurrentCitySearcher.
    """

    searcher_by_name = {
        'geocoder': GeocoderSearcher,
        'ipinfo': IpInfoSearcher,
    }
    return searcher_by_name.get(name)()


def get_storage(name: str) -> Storage:
    """
        Получает экземпляр объекта Storage по имени.

        Args:
            name (str): Название типа хранилища.
        Returns:
            Storage: Экземпляр объекта Storage.
    """

    searcher_by_name = {
        'json': JsonStorage,
        'sqlite': SQLiteStorage,
    }
    return searcher_by_name.get(name)()


def get_parser(name: str) -> Parser:
    """
        Получает экземпляр объекта Parser по имени.

        Args:
            name (str): Название парсера.
        Returns:
            Parser: Экземпляр объекта Parser.
    """

    searcher_by_name = {
        'standard': StandardParser,
    }
    return searcher_by_name.get(name)()


@main_menu_error_handler
def main() -> None:
    """
    Эта функция является основной точкой входа в приложение.

    Инициализирует объекты и запускает функцию, для отображения меню и
    предоставления выбора действия

    Returns:
        None
    """

    weather_searcher = get_weather_searcher('open_weather_api')
    current_city_searcher = get_current_city_searcher('geocoder')
    parser = get_parser('standard')

    with get_storage('json') as storage_instance:
        app = WeatherApp(weather_searcher, current_city_searcher, storage_instance, parser)
        app.start()


if __name__ == '__main__':
    main()
