
from services.files import settings
from services.modules.raising_errors import main_menu_error_handler
from services.storages.storage_type import StorageType
from services.modules.weather_app import WeatherApp
from services.modules.factory import Factory


@main_menu_error_handler
def main() -> None:
    """
        Эта функция является основной точкой входа в приложение.

        Инициализирует объекты и запускает функцию, для отображения меню и
        предоставления выбора действия

        Returns:
            None
    """
    weather_searcher = Factory.get_weather_searcher('open_weather_api')
    current_city_searcher = Factory.get_current_city_searcher('ipinfo')
    parser = Factory.get_parser('standard')

    with Factory.get_storage(
            StorageType.JsonStorage,
            parser=parser,
            file_name=settings.STORAGE_JSON_FILE_NAME
    ) as storage_instance:
        app = WeatherApp(weather_searcher, current_city_searcher, storage_instance, parser)
        app.start()


if __name__ == '__main__':
    main()
