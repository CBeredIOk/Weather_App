
from services.modules.app_errors import main_menu_error_handler
from services.modules.get_api_weather_data import get_weather_data_in_my_location
from services.modules.get_api_weather_data import get_weather_data_in_city
from services.modules.storage_weather_data import delete_request_history
from services.modules.request_history_weather_data import print_data_weather_request
from services.app_classes.action_menu_class import MenuAction
from services.files import interface_text


@main_menu_error_handler
def main():
    """
    Эта функция является основной точкой входа в приложение.

    Она отображает меню опций для выбора пользователем и
    обрабатывает вводимые им данные.

    Returns:
        None
    """
    while True:
        print(interface_text.MAIN_MENU)
        message_type = input(interface_text.OPTIONS).strip()
        COMMAND_DISPATCH_DICT[MenuAction(message_type)]()


def exit_function() -> None:
    """
    Функция выхода из приложения.

    Returns:
        None
    """
    print(interface_text.EXIT)
    raise SystemExit()


COMMAND_DISPATCH_DICT = ({
    MenuAction.WEATHER_IN_MY_LOCATION: get_weather_data_in_my_location,
    MenuAction.WEATHER_IN_SOME_CITY: get_weather_data_in_city,
    MenuAction.PRINT_REQUEST_HISTORY: print_data_weather_request,
    MenuAction.DELETE_HISTORY: delete_request_history,
    MenuAction.EXIT: exit_function,
})


if __name__ == '__main__':
    main()
