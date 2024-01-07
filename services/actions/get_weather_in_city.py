
from services.files import interface_text
from services.modules.raising_errors import error_handler

from services.actions.contracts import Action

from services.weather_searchers.contracts import WeatherSearcher
from services.storages.contracts import Storage
from services.parsers.contracts import Parser


class GetWeatherInCityAction(Action):
    """
        Класс GetWeatherInCityAction реализует действие получения погоды в указанном городе.

        Args:
            weather_searcher (WeatherSearcher): Объект для выполнения поиска погоды.
            storage (Storage): Объект для сохранения данных о погоде.
            parser (Parser): Объект для парсинга информации о погоде.
    """

    def __init__(
            self,
            weather_searcher: WeatherSearcher,
            storage: Storage,
            parser: Parser
    ):
        self.weather_searcher = weather_searcher
        self.storage = storage
        self.parser = parser

    @error_handler
    def run(self) -> None:
        """
            Запускает выполнение действия - получение и сохранение данных о погоде в указанном городе.

            Returns:
                None
        """

        city_name = input(interface_text.ENTER_CITY).strip()
        weather_data = self.weather_searcher.get_weather(city_name)
        weather_info = self.parser.parsing_weather_data(weather_data)
        print(weather_info)
        self.storage.save_data_weather(weather_info)
