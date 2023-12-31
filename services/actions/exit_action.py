
from services.actions.contracts import Action
from services.files import interface_text


class ExitAction(Action):
    def run(self) -> None:
        print(interface_text.EXIT)
        raise SystemExit()
