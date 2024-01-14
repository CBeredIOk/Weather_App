import datetime

from services.files import settings


def make_datetime_object(request_time: str, offset_from_utc: str) -> datetime.datetime:
    """
        Эта функция переводит время из timestep в формат datetime и показывает разницу по UTC

        Args:
            (request_time: str): время в городе при запросе
            (offset_from_utc: str): показывает разницу времени в городе от utc
        Returns:
            datetime: дата и время в городе при http запросе
    """

    timezone = datetime.timezone(datetime.timedelta(seconds=float(offset_from_utc)))
    return datetime.datetime.fromtimestamp(float(request_time), timezone)


def datetime_serializing(date: datetime.datetime) -> str:
    """
        Сериализует объект даты и времени в строку.

        Args:
            date (datetime.datetime): Объект даты и времени.
        Returns:
            str: Сериализованная строка с датой и временем.
    """

    if isinstance(date, datetime.datetime):
        # return date.replace(tzinfo=datetime.timezone.utc).strftime(settings.DATA_TYPE_PRINT)
        return date.strftime(settings.DATA_TYPE_PRINT)
    else:
        raise TypeError
