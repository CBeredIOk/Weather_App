
from services.files import interface_text
from services.modules.app_errors import error_handler
from services.modules.get_api_weather_data import print_weather_data_in_my_location
from services.modules.get_api_weather_data import print_weather_data_in_city
from services.modules.storage_weather_data import delete_request_history
from services.modules.request_history_weather_data import print_data_weather_request
from services.app_classes.action_menu import MenuAction


def exit_function() -> None:
    """
    Функция выхода из приложения.

    Returns:
        None
    """
    print(interface_text.EXIT)
    raise SystemExit()


COMMAND_DISPATCH = ({
    MenuAction.WEATHER_IN_MY_LOCATION: print_weather_data_in_my_location,
    MenuAction.WEATHER_IN_SOME_CITY: print_weather_data_in_city,
    MenuAction.PRINT_REQUEST_HISTORY: print_data_weather_request,
    MenuAction.DELETE_HISTORY: delete_request_history,
    MenuAction.EXIT: exit_function,
})


@error_handler
def execute_action_by_type(action_type: MenuAction) -> None:
    """
    Выполняет действие в соответствии с переданным типом действия из меню.

    Args:
        action_type (MenuAction): Тип действия из меню для выполнения.

    Returns:
        None
    """
    COMMAND_DISPATCH.get(action_type)()
