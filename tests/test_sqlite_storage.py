import pytest
import datetime

from services.modules.weather_info import WeatherInformation
from services.parsers.standard_parser import StandardParser
from services.storages.sqlite_storage import SQLiteStorage


weather_data_test_1 = WeatherInformation(
    date=datetime.datetime.fromisoformat('1111-11-11 11:11:11+11:00'),
    city_name='City_1',
    weather_conditions='Condition_1',
    temperature=-17,
    temperature_feels_like=-22,
    wind_speed=3)

weather_data_test_2 = WeatherInformation(
    date=datetime.datetime.fromisoformat('2222-02-22 22:22:22+02:00'),
    city_name='City_2',
    weather_conditions='Condition_2',
    temperature=13,
    temperature_feels_like=10,
    wind_speed=0)


@pytest.fixture
def storage(tmp_path):
    db_path = tmp_path / 'test_weather_app_data.db'
    with SQLiteStorage(parser=StandardParser, file_name=str(db_path)) as storage:
        yield storage


def test_save_data_weather(storage):

    # Arrange
    count_of_records = 1

    # Act
    storage.save_data_weather(weather_data_test_1)

    # Assert
    saved_data = storage.get_last_n_request(count_of_records)
    assert len(saved_data) == 1
    saved_weather_data = next(iter(saved_data.values()))
    assert saved_weather_data == weather_data_test_1


def test_get_last_n_request(storage):

    # Arrange
    count_of_records = 2
    storage.save_data_weather(weather_data_test_1)
    storage.save_data_weather(weather_data_test_2)

    # Act
    saved_data = storage.get_last_n_request(count_of_records)

    # Assert
    assert len(saved_data) == 2
    assert saved_data[1] == weather_data_test_1
    assert saved_data[2] == weather_data_test_2


def test_delete_request_history(storage):

    # Arrange
    count_of_records = 1
    storage.save_data_weather(weather_data_test_1)

    # Act
    storage.delete_request_history()

    # Assert
    saved_data = storage.get_last_n_request(count_of_records)
    assert len(saved_data) == 0
