
from services.actions.contracts import Action
from services.files import interface_text
from services.storages.contracts import Storage


class DeleteHistoryAction(Action):
    def __init__(self, storage: Storage):
        self.storage = storage

    def run(self):
        self.storage.delete_request_history()
        print(interface_text.ALL_REMOVED)
