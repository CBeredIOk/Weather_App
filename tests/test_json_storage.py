
import pytest
import datetime
import json

from services.modules.weather_info import WeatherInformation
from services.parsers.standard_parser import StandardParser
from services.storages.json_storage import JsonStorage


# Define test data
weather_data_test_1 = WeatherInformation(
    date=datetime.datetime.fromisoformat('1111-11-11 11:11:11+11:00'),
    city_name='City_1',
    weather_conditions='Condition_1',
    temperature=-17,
    temperature_feels_like=-22,
    wind_speed=3
)

weather_data_test_2 = WeatherInformation(
    date=datetime.datetime.fromisoformat('2222-02-22 22:22:22+02:00'),
    city_name='City_2',
    weather_conditions='Condition_2',
    temperature=13,
    temperature_feels_like=10,
    wind_speed=0
)


@pytest.fixture
def json_storage(tmp_path):
    file_path = tmp_path / 'test_weather_data.json'
    with open(file_path, 'w') as file:
        json.dump({}, file)
    with JsonStorage(parser=StandardParser, file_name=str(file_path)) as storage:
        yield storage


def test_save_data_weather(json_storage):

    # Act
    json_storage.save_data_weather(weather_data_test_1)

    # Assert
    saved_data = json_storage.get_last_n_request(1)
    assert len(saved_data) == 1
    assert 1 in saved_data
    saved_weather_data = saved_data[1]
    assert saved_weather_data == weather_data_test_1


def test_get_last_n_request(json_storage):

    # Arrange
    json_storage.save_data_weather(weather_data_test_1)
    json_storage.save_data_weather(weather_data_test_2)

    # Act
    saved_data = json_storage.get_last_n_request(n=2)

    # Assert
    assert len(saved_data) == 2
    assert 1 in saved_data
    assert 2 in saved_data
    assert saved_data[1] == weather_data_test_1
    assert saved_data[2] == weather_data_test_2


def test_delete_request_history(json_storage):

    # Arrange
    json_storage.save_data_weather(weather_data_test_1)

    # Act
    json_storage.delete_request_history()

    # Assert
    saved_data = json_storage.read_all_data_from_json()
    assert len(saved_data) == 0
