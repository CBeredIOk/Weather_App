
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


class NoStorageImplError(Exception):
    def __init__(self):
        super().__init__(interface_text.NoStorageImplError_TEXT)


class EmptyStorageError(Exception):
    def __init__(self):
        super().__init__(interface_text.EmptyStorageError_TEXT)
