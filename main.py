
from services.modules.app_api import execute_action_by_type
from services.modules.app_errors import main_menu_error_handler
from services.app_classes.action_menu import MenuAction
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
        action_type = MenuAction(message_type)
        execute_action_by_type(action_type)


if __name__ == '__main__':
    main()
