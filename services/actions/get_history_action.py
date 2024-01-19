
from services.files import interface_text

from services.actions.contracts import Action
from services.modules.custom_errors import EmptyStorageError
from services.modules.raising_errors import error_handler

from services.storages.contracts import Storage


class GetHistoryAction(Action):
    """
        Класс GetHistoryAction реализует действие вывода истории запросов о погоде.

        Args:
            storage (Storage): Объект для доступа к сохраненным данным о погоде.
        Attributes:
            weather_data_request (dict): Словарь с информацией о погоде.
            count_records_for_print (int): Количество записей для вывода.
            number_of_last_record (int): Номер последней записи.
    """

    def __init__(self, storage: Storage):
        self.storage = storage
        self.weather_data_request = None
        self.count_records_for_print = 0
        self.number_of_last_record = 0

    def print_n_request(self) -> None:
        """
            Выводит заданное количество последних записей о погоде.

            Returns:
                None
        """

        number_of_early_record = self.number_of_last_record - self.count_records_for_print
        for number_of_record in range(self.number_of_last_record, number_of_early_record, -1):
            weather_data = self.weather_data_request[number_of_record]
            print(weather_data)

    def print_all_request(self) -> None:
        """
            Выводит всю доступную историю запросов о погоде.

            Returns:
                None
        """

        for number_of_record in range(self.number_of_last_record, 0, -1):
            weather_data = self.weather_data_request[number_of_record]
            print(weather_data)

    @error_handler
    def process_weather_data_request(self) -> None:
        """
            Обрабатывает запрос данных о погоде.

            Проверяет количество полученных записей о погоде и выполняет соответствующие действия:
            - Если количество записей равно self.count_records_for_print, вызывается метод self.print_n_request().
            - Если количество записей меньше self.count_records_for_print, выводится сообщение о печати всех запросов
              и вызывается метод self.print_all_request().
            - Если нет записей, выбрасывается исключение EmptyStorageError.

            Returns:
                None
        """
        try:
            self.number_of_last_record = next(iter(self.weather_data_request))
            total_count = len(self.weather_data_request)
            if total_count == self.count_records_for_print:
                self.print_n_request()
            elif total_count < self.count_records_for_print:
                print(interface_text.PRINTED_ALL_REQUESTS + str(self.number_of_last_record))
                self.print_all_request()
        except StopIteration:
            raise EmptyStorageError

    def run(self) -> None:
        """
            Запускает выполнение действия - вывод истории запросов о погоде.

            Returns:
                None
        """

        self.count_records_for_print = int(input(interface_text.NUMBER_OF_REQUEST).strip())
        if self.count_records_for_print <= 0:
            raise ValueError
        else:
            self.weather_data_request = self.storage.get_last_n_request(self.count_records_for_print)
            self.process_weather_data_request()
