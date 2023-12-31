
from services.actions.contracts import Action
from services.actions.delete_history_action import DeleteHistoryAction
from services.actions.exit_action import ExitAction
from services.actions.get_history_action import GetHistoryAction
from services.actions.get_weather_in_city import GetWeatherInCityAction
from services.actions.get_weather_in_my_location import GetWeatherInMyLocationAction
from services.modules.action_menu import MenuAction
from services.current_city_searchers.contracts import CurrentCitySearcher
from services.parsers.contracts import Parser
from services.storages.contracts import Storage
from services.weather_searchers.contracts import WeatherSearcher


class ActionManager:
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

        self.COMMAND_DISPATCH = self.initialize_commands()

    def initialize_commands(self) -> dict[MenuAction: Action]:
        command_dispatch = {
            MenuAction.WEATHER_IN_MY_LOCATION: GetWeatherInMyLocationAction(
                self.weather_searcher,
                self.current_city_searcher,
                self.storage,
                self.parser,
            ),
            MenuAction.WEATHER_IN_SOME_CITY: GetWeatherInCityAction(self.weather_searcher, self.storage, self.parser),
            MenuAction.PRINT_REQUEST_HISTORY: GetHistoryAction(self.storage),
            MenuAction.DELETE_HISTORY: DeleteHistoryAction(self.storage),
            MenuAction.EXIT: ExitAction(),
        }
        return command_dispatch

    def execute(self, action_type: MenuAction) -> None:
        """
        Выполняет действие в соответствии с переданным типом действия из меню.

        Args:
            action_type (MenuAction): Тип действия из меню для выполнения.

        Returns:
            None
        """
        action = self.COMMAND_DISPATCH.get(action_type)
        action.run()
