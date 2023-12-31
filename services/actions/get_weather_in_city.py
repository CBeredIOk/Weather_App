
from services.actions.contracts import Action
from services.files import interface_text
from services.parsers.contracts import Parser
from services.storages.contracts import Storage
from services.weather_searchers.contracts import WeatherSearcher


class GetWeatherInCityAction(Action):
    def __init__(
            self,
            weather_searcher: WeatherSearcher,
            storage: Storage,
            parser: Parser
    ):
        self.weather_searcher = weather_searcher
        self.storage = storage
        self.parser = parser

    def run(self):
        city_name = input(interface_text.ENTER_CITY).strip()
        weather_data = self.weather_searcher.get_weather(city_name)
        weather_info = self.parser.parsing_weather_data(weather_data)
        print(weather_info)
        self.storage.save_data_weather(weather_info)
