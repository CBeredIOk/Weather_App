from services.current_city_searchers.contracts import CurrentCitySearcher
from services.current_city_searchers.geocoder_searcher import GeocoderSearcher
from services.current_city_searchers.ip_info_searcher import IpInfoSearcher

from services.parsers.contracts import Parser
from services.parsers.standard_parser import StandardParser

from services.storages.contracts import Storage
from services.storages.json_storage import JsonStorage
from services.storages.sqlite_storage import SQLiteStorage
from services.storages.storage_type import StorageType
from services.modules.custom_errors import NoStorageImplError

from services.weather_searchers.contracts import WeatherSearcher
from services.weather_searchers.open_weather_api_searcher import OpenWeatherAPISearcher


class Factory:
    """
        Фабрика для создания объектов различных типов (WeatherSearcher, CurrentCitySearcher, Parser, и Storage).

    """

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_storage(storage_type: StorageType, **kwargs) -> Storage:
        """
            Возвращает экземпляр объекта хранилища (Storage) в зависимости от указанного типа.

            Args:
                storage_type (StorageType): Тип хранилища (StorageType), определенный в перечислении StorageType.
                **kwargs: Дополнительные аргументы, которые передаются конструктору хранилища (такие как Parser,
                file_name).
            Returns:
                Storage: Экземпляр объекта хранилища соответствующего типа.
        """

        storages_for_type = {
            StorageType.JsonStorage: JsonStorage,
            StorageType.SQLiteStorage: SQLiteStorage,
        }
        try:
            return storages_for_type[storage_type](**kwargs)
        except KeyError:
            raise NoStorageImplError()
