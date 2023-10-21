
import os
import json
import datetime
from typing import Any

from Weather_App.files import settings
from .app_errors import error_handler
from .app_errors import OpenStorageError, SaveStorageError


@error_handler
def read_all_data_from_storage() -> Any:
    """
    Эта функция считывает всю историю запросов с файла json.

    Returns:
        Any: возвращает информацию с json файла
    """
    try:
        with open(find_storage_path(), 'r+') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        raise OpenStorageError


@error_handler
def write_new_data_to_storage(data: dict[str, Any]) -> None:
    """
    Эта функция записывает новую информацию в файл json.

    Args:
        (data: dict[str, Any]): словарь с новой информацией для записи.
    Returns:
        None
    """
    try:
        with open(find_storage_path(), 'w+') as json_file:
            json.dump(data, json_file, indent=4, default=datetime_serializer)
    except FileNotFoundError:
        raise SaveStorageError


def find_storage_path() -> str:
    """
    Эта функция находит путь к файлу json.

    Функция поиска поднимается до Weather_App и потом переходит в папку хранения STORAGE_FOLDER

    Returns:
        str: возвращает путь в виде строки
    """
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)

    json_file_path = os.path.join(grandparent_dir, settings.STORAGE_FOLDER, settings.STORAGE_FILE_NAME)
    return json_file_path


def datetime_serializer(date: datetime.datetime) -> str:
    """
    Сериализует объект datetime.datetime в строку с заданным форматом.

    Args:
        date (datetime.datetime): Объект datetime.datetime для сериализации.
    Returns:
        str: Строка, представляющая дату и время в указанном формате.
    """
    if isinstance(date, datetime.datetime):
        return date.strftime(settings.DATA_TYPE_PRINT)
    raise TypeError
