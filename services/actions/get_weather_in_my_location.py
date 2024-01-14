
from services.actions.contracts import Action

from services.weather_searchers.contracts import WeatherSearcher
from services.current_city_searchers.contracts import CurrentCitySearcher
from services.storages.contracts import Storage
from services.parsers.contracts import Parser


class GetWeatherInMyLocationAction(Action):
    """
        Класс GetWeatherInMyLocationAction реализует действие получения погоды в текущем местоположении.

        Args:
            weather_searcher (WeatherSearcher): Объект для выполнения поиска погоды.
            current_city_searcher (CurrentCitySearcher): Объект для поиска текущего города.
            storage (Storage): Объект для сохранения данных о погоде.
            parser (Parser): Объект для парсинга информации о погоде.
    """

    def __init__(
            self,
            weather_searcher: WeatherSearcher,
            current_city_searcher: CurrentCitySearcher,
            storage: Storage,
            parser: Parser,
    ):
        self.weather_searcher = weather_searcher
        self.current_city_searcher = current_city_searcher
        self.storage = storage
        self.parser = parser

    def run(self) -> None:
        """
            Запускает выполнение действия - получение и сохранение данных о погоде в текущем местоположении.

            Returns:
                None
        """

        current_city = self.current_city_searcher.get_current_city()
        weather_data = self.weather_searcher.get_weather(current_city)
        weather_info = self.parser.parsing_weather_data_from_request(weather_data)
        print(weather_info)
        self.storage.save_data_weather(weather_info)
