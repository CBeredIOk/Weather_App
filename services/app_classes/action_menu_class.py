
from enum import StrEnum


class MenuAction(StrEnum):
    WEATHER_IN_MY_LOCATION = '1'
    WEATHER_IN_SOME_CITY = '2'
    PRINT_REQUEST_HISTORY = '3'
    DELETE_HISTORY = '4'
    EXIT = '5'
