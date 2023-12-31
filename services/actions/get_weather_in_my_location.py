from services.actions.contracts import Action
from services.current_city_searchers.contracts import CurrentCitySearcher
from services.parsers.contracts import Parser
from services.storages.contracts import Storage
from services.weather_searchers.contracts import WeatherSearcher


class GetWeatherInMyLocationAction(Action):
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

    def run(self):
        current_city = self.current_city_searcher.get_current_city()
        weather_data = self.weather_searcher.get_weather(current_city)
        weather_info = self.parser.parsing_weather_data(weather_data)
        print(weather_info)
        self.storage.save_data_weather(weather_info)
