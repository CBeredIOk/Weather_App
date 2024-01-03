
from services.files import interface_text


class ApiRequestError(Exception):
    def __init__(self):
        super().__init__(interface_text.ApiRequestError_TEXT)


class MissCityError(Exception):
    def __init__(self):
        super().__init__(interface_text.MissCityError_TEXT)


class SaveStorageError(Exception):
    def __init__(self):
        super().__init__(interface_text.SaveStorageError_TEXT)


class OpenStorageError(Exception):
    def __init__(self):
        super().__init__(interface_text.OpenStorageError_TEXT)


class GeocoderError(Exception):
    def __init__(self):
        super().__init__(interface_text.GeocoderError_TEXT)


class LostConnectionError(Exception):
    def __init__(self):
        super().__init__(interface_text.LostConnectionError_TEXT)


class DatabaseException(Exception):
    def __init__(self):
        super().__init__(interface_text.DatabaseException_TEXT)


def print_error_message(error_message: str) -> None:
    """
        Выводит сообщение об ошибке в красном цвете в консоли.

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
