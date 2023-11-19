
import unittest
import datetime

from services.app_classes.weather_info import WeatherInformation
from services.modules.process_weather_data import make_datetime_object, parse_weather_data


class TestMakeDatetimeObject(unittest.TestCase):

    def test_assert_object_type(self):
        # Arrange
        request_time = '1634550000'
        timedelta_seconds = '3600'
        expected_datetime = datetime.datetime(
            2021, 10, 18, 10, 40,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=float(timedelta_seconds)))
        )

        # Act
        sut = make_datetime_object(request_time, timedelta_seconds)

        # Assert
        self.assertEqual(type(expected_datetime), type(sut))

    def test_assert_datetime_object(self):
        # Arrange
        request_time = '1634550000'
        timedelta_seconds = '3600'
        expected_datetime = datetime.datetime(
            2021, 10, 18, 10, 40,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=float(timedelta_seconds)))
        )

        # Act
        sut = make_datetime_object(request_time, timedelta_seconds)

        # Assert
        self.assertEqual(expected_datetime, sut)


class TestParseWeatherData(unittest.TestCase):

    def test_parse_weather_data(self):
        # Arrange
        request_time = '1634550000'
        timedelta_seconds = '3600'
        expected_datetime = datetime.datetime(
            2021, 10, 18, 10, 40,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=float(timedelta_seconds)))
        )
        weather_data = {
            'dt': request_time,
            'timezone': timedelta_seconds,
            'name': 'Рим',
            'weather': [{'description': 'ясно'}],
            'main': {'temp': '18', 'feels_like': '20'},
            'wind': {'speed': '10'},
        }

        # Act
        sut = parse_weather_data(weather_data)

        # Assert
        self.assertIsInstance(sut, WeatherInformation)

        self.assertEqual(sut.date, expected_datetime)
        self.assertEqual(sut.city_name, 'Рим')
        self.assertEqual(sut.weather_conditions, 'ясно')
        self.assertEqual(sut.temperature, 18)
        self.assertEqual(sut.temperature_feels_like, 20)
        self.assertEqual(sut.wind_speed, 10)


if __name__ == '__main__':
    unittest.main()
