
import ipinfo

from services.files import settings


class IpInfoSearcher:
    @staticmethod
    def get_current_city() -> str:
        handler = ipinfo.getHandler(settings.IPINFO_API_KEY)
        details = handler.getDetails('')
        city_name = details.all.get('city')
        return city_name
