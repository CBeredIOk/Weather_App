
from services.files import interface_text

from services.actions.contracts import Action

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

    def print_request_history(self) -> None:
        """
            Определяет, какую историю запросов следует вывести.

            Returns:
                None
        """

        self.number_of_last_record = next(iter(self.weather_data_request))
        if len(self.weather_data_request) == self.count_records_for_print:
            self.print_n_request()
        elif len(self.weather_data_request) < self.count_records_for_print:
            print(interface_text.PRINTED_ALL_REQUESTS + str(self.number_of_last_record))
            self.print_all_request()

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
            self.print_request_history()
