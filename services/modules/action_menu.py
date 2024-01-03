
from enum import StrEnum


class MenuAction(StrEnum):
    """
    Перечисление MenuAction представляет типы действий меню приложения.

    Каждый элемент перечисления соответствует определенному действию в меню
    приложения для отображения погоды.

    Attributes:
        WEATHER_IN_MY_LOCATION (str): Запрос погоды по текущему местоположению.
        WEATHER_IN_SOME_CITY (str): Запрос погоды для определенного города.
        PRINT_REQUEST_HISTORY (str): Вывод истории запросов погоды.
        DELETE_HISTORY (str): Удаление истории запросов погоды.
        EXIT (str): Выход из приложения.
    """

    WEATHER_IN_MY_LOCATION = '1'
    WEATHER_IN_SOME_CITY = '2'
    PRINT_REQUEST_HISTORY = '3'
    DELETE_HISTORY = '4'
    EXIT = '5'
