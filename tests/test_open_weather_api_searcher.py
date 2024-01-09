import pytest

from services.files.interface_text import MissCityError_TEXT
from services.modules.custom_errors import MissCityError
from services.weather_searchers.open_weather_api_searcher import OpenWeatherAPISearcher


def test_get_weather_successful_response():

    # Arrange
    location = 'Rim'
    excepted_city_name = 'Рим'
    weather_searcher = OpenWeatherAPISearcher()

    # Act
    actual_weather_data = weather_searcher.get_weather(location)

    # Assert
    assert actual_weather_data['name'] == excepted_city_name
    assert actual_weather_data['cod'] == 200


def test_raise_not_found_error():

    # Arrange
    location = 'Not_Exist_City_404'
    weather_searcher = OpenWeatherAPISearcher()

    # Act
    with pytest.raises(MissCityError) as exc_info:
        weather_searcher.get_weather(location)

    # Assert
    assert str(exc_info.value) == MissCityError_TEXT
