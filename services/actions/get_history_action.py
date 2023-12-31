from services.actions.contracts import Action
from services.files import interface_text
from services.storages.contracts import Storage


class GetHistoryAction(Action):
    def __init__(self, storage: Storage):
        self.storage = storage

    def run(self):
        count_of_records = int(input(interface_text.NUMBER_OF_REQUEST).strip())
        if count_of_records < 0:
            print(interface_text.ValueError_TEXT)
        else:
            weather_data_request = self.storage.get_last_n_request(count_of_records)
            number_of_records = next(iter(weather_data_request))
            if len(weather_data_request) == count_of_records:
                for number_of_record in range(number_of_records, number_of_records - count_of_records, -1):
                    weather_data = weather_data_request[number_of_record]
                    print(weather_data)
            else:
                print(interface_text.PRINTED_ALL_REQUESTS + str(number_of_records))
                for number_of_record in range(number_of_records, 0, -1):
                    weather_data = weather_data_request[number_of_record]
                    print(weather_data)
