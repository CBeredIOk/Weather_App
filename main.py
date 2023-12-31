
from services.modules.app_errors import main_menu_error_handler

from services.current_city_searchers.contracts import CurrentCitySearcher
from services.current_city_searchers.geocoder_searcher import GeocoderSearcher
from services.current_city_searchers.ip_info_searcher import IpInfoSearcher
from services.parsers.contracts import Parser
from services.parsers.standard_parser import StandardParser

from services.storages.contracts import Storage
from services.storages.json_storage import JsonStorage
from services.storages.sqlite_storage import SQLiteStorage

from services.weather_searchers.contracts import WeatherSearcher
from services.weather_searchers.open_weather_api_searcher import OpenWeatherAPISearcher

from services.modules.weather_app import WeatherApp


def get_weather_searcher(name: str) -> WeatherSearcher:
    searcher_by_name = {
        'open_weather_api': OpenWeatherAPISearcher,
    }
    return searcher_by_name.get(name)()


def get_current_city_searcher(name: str) -> CurrentCitySearcher:
    searcher_by_name = {
        'geocoder': GeocoderSearcher,
        'ipinfo': IpInfoSearcher,
    }
    return searcher_by_name.get(name)()


def get_storage(name: str) -> Storage:
    searcher_by_name = {
        'json': JsonStorage,
        'sqlite': SQLiteStorage,
    }
    return searcher_by_name.get(name)()


def get_parser(name: str) -> Parser:
    searcher_by_name = {
        'standard': StandardParser,
    }
    return searcher_by_name.get(name)()


@main_menu_error_handler
def main():
    """
    Эта функция является основной точкой входа в приложение.

    Она отображает меню опций для выбора пользователем и
    обрабатывает вводимые им данные.

    Returns:
        None
    """
    weather_searcher = get_weather_searcher('open_weather_api')
    current_city_searcher = get_current_city_searcher('geocoder')
    storage = get_storage('sqlite')
    parser = get_parser('standard')

    app = WeatherApp(weather_searcher, current_city_searcher, storage, parser)
    app.start()


if __name__ == '__main__':
    main()
