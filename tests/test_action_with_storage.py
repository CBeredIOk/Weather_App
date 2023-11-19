
import unittest
import json
from services.modules.action_with_storage import write_new_data_to_storage


class TestWriteNewDataToStorage(unittest.TestCase):
    def test_writing_to_storage(self):
        # Arrange
        test_data = {
            '1': {
                'date': '2023-11-19 10:56:20', 'city_name': 'Санкт-Петербург', 'weather_conditions': 'ясно',
                'temperature': -4, 'temperature_feels_like': -8, 'wind_speed': 2
            },
        }

        # Act
        write_new_data_to_storage(test_data)

        # Assert
        with open(
                'C:\\Users\\zhsve\\PycharmProjects\\homework\\'
                'Weather_App\\services\\files\\weather_history_request.json',
                'r'
        ) as json_file:
            stored_data = json.load(json_file)

        self.assertEqual(stored_data, test_data)


if __name__ == '__main__':
    unittest.main()
