import datetime
import json
from http import HTTPStatus

import geocoder
import requests
from requests.exceptions import RequestException

import settings


def get_weather_data(location: str) -> dict[str, str]:
    """
    Эта функция отправляет http запрос и записывает полученную информацию в словарь.

    Args:
        (location: str): Название города, по которому будет отправлен http запрос.
    Returns:
        dict[str, str]: Словарь с полученной информацией о погоде в городе.
    """
    api_url = settings.API_GET_REQUEST_CITY_WEATHER.format(location=location, api_key=settings.API_KEY)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except RequestException as error:
        return {'message': 'во время выполнения запроса', 'cod': error}
    except json.JSONDecodeError as error:
        return {'message': 'во время разбора JSON', 'cod': error}

    dt = data['dt']
    timezone = data['timezone']
    name = data['name']
    temperature = round(data['main']['temp'] - settings.TO_CELSIUS)
    feels_like = round(data["main"]['feels_like'] - settings.TO_CELSIUS)
    weather = data['weather'][0]['description']
    wind_speed = round(data['wind']['speed'])
    cod = data['cod']

    return {
        'dt': dt, 'timezone': timezone, 'city': name, 'weather': weather, 'temperature': temperature,
        'feels_like': feels_like, 'wind_speed': wind_speed, 'cod': cod
    }


def processing_data_weather(weather_data: dict[str, str]):
    """
    Эта функция отправляет информацию в словаре на печать в функцию print_data_weather()
    и потом на запись в json файл через функцию remembering_data_weather().

    Args:
        (weather_data: dict[str, str]): Словарь с информацией о погоде в городе.
    Returns:
        None
    """
    if weather_data['cod'] == HTTPStatus.OK:
        print_data_weather(weather_data)
        remembering_data_weather(weather_data)
    else:
        print(f'Ошибка: {weather_data["message"]}. Код ошибки: {weather_data["cod"]}')


def print_data_weather(weather_data_to_print: dict[str, str]):
    """
    Эта функция выводит в консоль информацию о погоде из принимаемого словаря.

    Args:
        (weather_data_to_print: dict[str, str]): Словарь с информацией о погоде в городе.
    Returns:
        None
    """
    print(f'\nТекущее время: {make_datetime_object(weather_data_to_print["dt"], weather_data_to_print["timezone"])}')
    print(f'Название города: {weather_data_to_print["city"]}')
    print(f'Погодные условия: {weather_data_to_print["weather"]}')
    print(f'Текущая температура: {weather_data_to_print["temperature"]} градусов по цельсию')
    print(f'Ощущается как: {weather_data_to_print["feels_like"]} градусов по цельсию')
    print(f'Скорость ветра: {weather_data_to_print["wind_speed"]} м/с\n')


def make_datetime_object(request_time: str, timedelta_seconds: str) -> datetime:
    """
    Эта функция переводит время из timestep в формат datetime и показывает разницу по UTC

    Args:
        (request_time: str): время в городе при запросе
        (timedelta_seconds: str): показывает разницу времени в городе от 0 часового пояса
    Returns:
        datetime: дата и время в городе при http запросе
    """
    timezone = datetime.timezone(datetime.timedelta(seconds=float(timedelta_seconds)))
    return datetime.datetime.fromtimestamp(float(request_time), timezone)


def remembering_data_weather(weather_data_to_history: dict[str, str]):
    """
    Эта функция сохраняет информацию о погоде из принимаемого словаря в json файл.

    Args:
        (weather_data_to_history: dict[str, str]): Словарь с информацией о погоде в городе.
    Returns:
        None
    """
    try:
        with open('request_weather_history.json', 'r') as json_file:
            existing_data = json.load(json_file)
        existing_data[str(len(existing_data) + 1)] = weather_data_to_history
        with open('request_weather_history.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f'Ошибка при чтении файла: {error}')


def print_last_n_weather_request(count_of_records: int):
    """
    Эта функция выводит информацию последних n запросов.

    Args:
        (count_of_records: int): Число последних записей для вывода.
    Returns:
        None
    """
    with open('request_weather_history.json', 'r') as json_file:
        all_weather_data = json.load(json_file)
    try:
        number_of_records = len(all_weather_data) + 1
        for number_of_record in range(number_of_records - count_of_records, number_of_records):
            weather_data = all_weather_data[str(number_of_record)]
            print_data_weather(weather_data)
    except KeyError:
        print(f'\n!!! Ошибка. {count_of_records} - такого количества записей нет !!! ')


def delete_request_history():
    """
    Эта функция позволяет очищать файл с историей запросов.

    Returns:
        None
    """
    empty_dictionary = {}
    with open('request_weather_history.json', 'w') as json_file:
        json.dump(empty_dictionary, json_file)
    print('Все запросы из истории удалены')


def main():
    """
    Эта функция является основной точкой входа в приложение.

    Она отображает меню опций для выбора пользователем и
    обрабатывает вводимые данные.

    Returns:
        None
    """
    print(
        'Варианты действий в приложении: 1 - Погода в моем местоположении, 2 - Погода в городе,'
        ' 3 - История запросов, 4 - удаление всех запросов из истории, 5 - Выход',
    )
    while True:
        match input('Введите действие (1, 2, 3, 4, 5): '):
            case '1':
                city = geocoder.ip('me').city
                processing_data_weather(get_weather_data(city))
            case '2':
                city = input('Введите город: ')
                processing_data_weather(get_weather_data(city))
            case '3':
                record_count = input('Введите сколько последних записей вывести: ')
                try:
                    print_last_n_weather_request(int(record_count))
                except ValueError:
                    print(f'\n!!! Ошибка. "{record_count}" - не integer !!! ')
            case '4':
                delete_request_history()
            case '5':
                print('Выход из программы')
                break
            case _:
                print('Некорректный ввод, попробуйте ещё раз')


if __name__ == '__main__':
    main()
