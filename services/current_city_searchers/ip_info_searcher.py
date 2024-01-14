
import ipinfo

from services.files import settings


class IpInfoSearcher:
    """
        Класс IpInfoSearcher реализует поиск текущего города с использованием IpInfo.

    """

    @staticmethod
    def get_current_city() -> str:
        """
            Возвращает название текущего города, основываясь на данных от IpInfo.

            Returns:
                str: Название текущего города.
        """

        handler = ipinfo.getHandler(settings.IPINFO_API_KEY)
        details = handler.getDetails('')
        city_name = details.all.get('city')
        return city_name
