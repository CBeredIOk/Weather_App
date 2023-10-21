
from Weather_App.files import interface_text
from .app_errors import error_handler
from Weather_App.services.app_classes.WeatherInfoClass import WeatherInformation
from .action_with_json import write_new_data_to_storage
from .action_with_json import read_all_data_from_storage


@error_handler
def remembering_data_weather(weather_data_to_history: WeatherInformation) -> None:
    """
    Эта функция сохраняет информацию о погоде в json файл из принимаемого объекта с информацией о погоде.

    Args:
        (weather_data_to_history: WeatherInformation): объект с информацией о погоде.
    Returns:
        None
    """
    existing_data = read_all_data_from_storage()
    existing_data[str(len(existing_data) + 1)] = weather_data_to_history.to_dict()
    write_new_data_to_storage(existing_data)


def delete_request_history() -> None:
    """
    Эта функция позволяет очищать файл с историей запросов.

    Returns:
        None
    """
    empty_dictionary = {}
    write_new_data_to_storage(empty_dictionary)
    print(interface_text.ALL_REMOVED)
