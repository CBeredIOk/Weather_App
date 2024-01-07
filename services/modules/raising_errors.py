from http import HTTPStatus

from services.files import interface_text
from services.modules.custom_errors import (
    LostConnectionError,
    SaveStorageError,
    OpenStorageError,
    ApiRequestError,
    MissCityError,
    GeocoderError,
)


def raising_http_errors(status_code: int) -> None:
    """
    Проверяет код состояния HTTP и возбуждает соответствующие ошибки.

    Args:
        status_code (int): Код состояния HTTP.
    Returns:
        None
    """

    if status_code == HTTPStatus.NOT_FOUND or status_code == HTTPStatus.BAD_REQUEST:
        raise MissCityError
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise ApiRequestError


def print_error_message(error_message: str) -> None:
    """
        Выводит сообщение об ошибке в консоли в красном цвете.

        Args:
            error_message (str): Сообщение об ошибке для вывода в консоли.
        Returns:
            None
    """
    print(f'{interface_text.RED_COLOR}{error_message}{interface_text.RESET_COLOR}')


def error_handler(func):
    """
        Обработчик ошибок для функций

        Перехватывает определенные исключения и пробрасывает их к обработчику ошибок главного меню.

    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (
            MissCityError, ApiRequestError, GeocoderError,
            SaveStorageError, OpenStorageError, LostConnectionError,
            TypeError, ValueError
        ) as error:
            raise error
        else:
            return result
    return wrapper


def main_menu_error_handler(func):
    """
        Обработчик ошибок для главного меню/пользовательского ввода, выводит сообщения об ошибках определенных типов.

    """

    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (
                    MissCityError, ApiRequestError, GeocoderError,
                    SaveStorageError, OpenStorageError, LostConnectionError,
            ) as error:
                print_error_message(str(error))
            except ValueError:
                print_error_message(interface_text.ValueError_TEXT)
            except TypeError:
                print_error_message(interface_text.TypeMenuError_TEXT)
            except TimeoutError:
                print_error_message(interface_text.TimeOutError_TEXT)
            except Exception:
                print_error_message(interface_text.ExceptionError_TEXT)
    return wrapper
