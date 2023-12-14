from typing import Protocol


class Storage(Protocol):
    def save(self, weather_info: dict) -> None:
        raise NotImplementedError

    def print_last_n(self, n: int) -> dict:
        raise NotImplementedError

    def delete_request_history(self) -> None:
        raise NotImplementedError
