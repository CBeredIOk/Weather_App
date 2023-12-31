
from typing import Protocol


class Action(Protocol):
    def run(self):
        raise NotImplementedError
