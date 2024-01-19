
import pytest
import json

from services.actions.get_history_action import GetHistoryAction
from services.parsers.standard_parser import StandardParser
from services.storages.json_storage import JsonStorage

from services.files.interface_text import EmptyStorageError_TEXT
from services.modules.custom_errors import EmptyStorageError
from services.storages.sqlite_storage import SQLiteStorage


@pytest.fixture
def json_storage(tmp_path):
    file_path = tmp_path / 'test_weather_data.json'
    with open(file_path, 'w') as file:
        json.dump({}, file)
    with JsonStorage(parser=StandardParser, file_name=str(file_path)) as storage:
        yield storage


def test_raise_json_storage_error(json_storage, monkeypatch):

    # Arrange
    getter_history_data = GetHistoryAction(json_storage)
    monkeypatch.setattr('builtins.input', lambda _: '5')

    # Act
    with pytest.raises(EmptyStorageError) as exc_info:
        getter_history_data.run()

    # Assert
    assert str(exc_info.value) == EmptyStorageError_TEXT


@pytest.fixture
def sqlite_storage(tmp_path):
    db_path = tmp_path / 'test_weather_app_data.db'
    with SQLiteStorage(parser=StandardParser, file_name=str(db_path)) as storage:
        yield storage


def test_raise_empty_storage_error(sqlite_storage, monkeypatch):

    # Arrange
    getter_history_data = GetHistoryAction(sqlite_storage)
    monkeypatch.setattr('builtins.input', lambda _: '5')

    # Act
    with pytest.raises(EmptyStorageError) as exc_info:
        getter_history_data.run()

    # Assert
    assert str(exc_info.value) == EmptyStorageError_TEXT


def test_raise_wrong_input_error(json_storage, monkeypatch):

    # Arrange
    getter_history_data = GetHistoryAction(json_storage)
    monkeypatch.setattr('builtins.input', lambda _: 'wrong_input')

    # Act & Assert
    with pytest.raises(ValueError):
        getter_history_data.run()
