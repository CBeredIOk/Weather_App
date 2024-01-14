
from enum import Enum


class StorageType(Enum):
    """
        Перечисление MenuAction представляет типы действий меню приложения.

        Каждый элемент перечисления соответствует определенному действию в меню
        приложения для отображения погоды.

        Attributes:
            JsonStorage (int):
            SQLiteStorage (int):
    """

    JsonStorage = 1
    SQLiteStorage = 2
