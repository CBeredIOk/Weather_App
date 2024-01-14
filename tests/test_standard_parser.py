
import datetime
import pytest

from services.parsers.standard_parser import StandardParser
from services.modules.weather_info import WeatherInformation


@pytest.fixture
def sample_weather_data_request():
    return {
        'dt': 1642156800,
        'timezone': 3600,
        'name': 'City',
        'weather': [{'description': 'Clear'}],
        'main': {'temp': 25, 'feels_like': 28},
        'wind': {'speed': 10}
    }


def test_parsing_weather_data_from_request(sample_weather_data_request):

    # Act
    parsed_data = StandardParser.parsing_weather_data_from_request(sample_weather_data_request)

    # Assert
    assert isinstance(parsed_data, WeatherInformation)
    assert parsed_data.date.year == 2022
    assert parsed_data.city_name == 'City'
    assert parsed_data.weather_conditions == 'Clear'
    assert parsed_data.temperature == 25
    assert parsed_data.temperature_feels_like == 28
    assert parsed_data.wind_speed == 10


def test_formoting_data_from_storage():

    # Arrange
    sample_weather_data_storage = {
        'date': '2022-02-22 22:00:22+03:00',
        'city_name': 'City',
        'weather_conditions': 'Clear',
        'temperature': 25,
        'temperature_feels_like': 28,
        'wind_speed': 10
    }

    date_to_assert = datetime.datetime(
        2022, 2, 22, 22, 0, 22,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))
    )

    # Act
    parsed_data = StandardParser.formoting_data_from_storage(sample_weather_data_storage)

    # Assert
    assert isinstance(parsed_data, WeatherInformation)
    assert parsed_data.date == date_to_assert
    assert parsed_data.city_name == 'City'
    assert parsed_data.weather_conditions == 'Clear'
    assert parsed_data.temperature == 25
    assert parsed_data.temperature_feels_like == 28
    assert parsed_data.wind_speed == 10
