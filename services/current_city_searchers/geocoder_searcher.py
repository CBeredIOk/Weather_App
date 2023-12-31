
import geocoder


class GeocoderSearcher:
    @staticmethod
    def get_current_city() -> str:
        city_name = geocoder.ip('me').city
        return city_name
