
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


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (
                MissCityError, ApiRequestError, GeocoderError,
                SaveStorageError, OpenStorageError, LostConnectionError
        ) as error:
            print(error)
        except TypeError:
            print(interface_text.TypeError_TEXT)
        except ValueError:
            print(interface_text.ValueError_TEXT)
        else:
            return result
    return wrapper


def main_menu_error_handler(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError:
                print(interface_text.TypeMenuError_TEXT)
            except TimeoutError:
                print(interface_text.TimeOutError_TEXT)
            except Exception:
                print(interface_text.ExceptionError_TEXT)
    return wrapper
