
import dataclasses
import datetime
from typing import Any

from files import interface_text


@dataclasses.dataclass
class WeatherInformation:
    """
    Класс, представляющий информацию о погоде.

    Attributes:
        date (str): Текущее время.
        city_name (str): Название города.
        weather_conditions (str): Погодные условия.
        temperature (int): Текущая температура в градусах по Цельсию.
        temperature_feels_like (int): Ощущаемая температура в градусах по Цельсию.
        wind_speed (int): Скорость ветра в м/с.
    """

    date: datetime.datetime
    city_name: str
    weather_conditions: str
    temperature: int
    temperature_feels_like: int
    wind_speed: int

    def __str__(self) -> str:
        """
        Возвращает строку с информацией о текущей погоде.

        Returns:
            str: Строка, содержащая информацию о погоде, включая текущее время,
            название города, погодные условия, температуру, ощущаемую температуру и скорость ветра.
        """

        string_weather_info = (
                interface_text.SEPARATION_LINE +
                interface_text.CURRENT_TIME + str(self.date) +
                interface_text.CITY_NAME + str(self.city_name) +
                interface_text.WEATHER_CONDITIONS + str(self.weather_conditions) +
                interface_text.TEMPERATURE + str(self.temperature) + interface_text.CELSIUS +
                interface_text.TEMPERATURE_FEELS_LIKE + str(self.temperature_feels_like) + interface_text.CELSIUS +
                interface_text.WIND_SPEED + str(self.wind_speed) + interface_text.MS +
                interface_text.SEPARATION_LINE
        )
        return string_weather_info

    def to_dict(self) -> dict[str, Any]:
        """
        Преобразует объект данных погоды в JSON-строку.

        Returns:
            dict[str, Any]: словарь, содержащий информацию о погоде.
        """
        return dataclasses.asdict(self)
