
from unittest.mock import patch
from services.modules.storage_weather_data import delete_request_history


def test_equal():
    assert 1 == 1


def test_not_equal():
    assert 1 != 0


def test_delete_request_history_prints_message(capsys):
    with patch('builtins.print') as mock_print:
        delete_request_history()
        mock_print.assert_called_once_with('\nВсе запросы из истории удалены ')
