
from services.files import interface_text

from services.actions.contracts import Action

from services.storages.contracts import Storage


class DeleteHistoryAction(Action):
    """
    Класс DeleteHistoryAction реализует действие удаления истории запросов о погоде.

    Args:
        storage (Storage): Объект для доступа к сохраненным данным о погоде.
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def run(self) -> None:
        """
            Удаляет всю историю запросов о погоде из хранилища.

            Returns:
                None
        """

        self.storage.delete_request_history()
        print(interface_text.ALL_REMOVED)
