
from services.modules.action_menu import MenuAction
from services.current_city_searchers.contracts import CurrentCitySearcher
from services.files import interface_text
from services.modules.action_manager import ActionManager
from services.parsers.contracts import Parser
from services.storages.contracts import Storage
from services.weather_searchers.contracts import WeatherSearcher


class WeatherApp:
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

    def start(self) -> None:
        action_manager = ActionManager(self.weather_searcher, self.current_city_searcher, self.storage, self.parser)
        while True:
            print(interface_text.MAIN_MENU)
            message_type = input(interface_text.OPTIONS).strip()
            action_type = MenuAction(message_type)
            action_manager.execute(action_type)
