
from services.files import interface_text

from services.modules.action_manager import ActionManager
from services.modules.action_menu import MenuAction

from services.weather_searchers.contracts import WeatherSearcher
from services.current_city_searchers.contracts import CurrentCitySearcher
from services.storages.contracts import Storage
from services.parsers.contracts import Parser


class WeatherApp:
    """
    Класс WeatherApp представляет приложение для отображения погоды.

    Этот класс управляет функциональностью приложения, включая поиск погоды,
    текущего города, хранение данных и парсинг информации.

    Args:
        weather_searcher (WeatherSearcher): Объект для поиска погоды.
        current_city_searcher (CurrentCitySearcher): Объект для поиска текущего города.
        storage (Storage): Объект для хранения данных.
        parser (Parser): Объект для парсинга информации.
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

    def start(self) -> None:
        """
        Прокручивает главное меню приложения и запрашивает выбор действия у пользователя.

        Returns:
            None
        """

        action_manager = ActionManager(self.weather_searcher, self.current_city_searcher, self.storage, self.parser)
        while True:
            print(interface_text.MAIN_MENU)
            message_type = input(interface_text.OPTIONS).strip()
            action_type = MenuAction(message_type)
            action_manager.execute(action_type)
