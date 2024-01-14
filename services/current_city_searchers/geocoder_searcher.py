
import geocoder


class GeocoderSearcher:
    """
        Класс GeocoderSearcher реализует поиск текущего города с использованием геокодера.

    """

    @staticmethod
    def get_current_city() -> str:
        """
            Возвращает название текущего города на основе IP-адреса.

            Returns:
                str: Название текущего города.
        """

        city_name = geocoder.ip('me').city
        return city_name
