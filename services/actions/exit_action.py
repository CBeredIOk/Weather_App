
from services.files import interface_text

from services.actions.contracts import Action


class ExitAction(Action):
    """
        Класс ExitAction реализует действие завершения приложения.

    """

    def run(self) -> None:
        """
            Выводит сообщение о выходе и вызывает SystemExit для завершения программы.

            Returns:
                None
        """

        print(interface_text.EXIT)
        raise SystemExit()
