from http import HTTPStatus
import requests
from requests.exceptions import RequestException
import geocoder
import datetime
import json
import settings


def get_weather_data(location: str) -> dict:
    api_url = settings.API_GET_REQUEST_WEATHER_IN_CITY.format(location=location, api_key=settings.API_KEY)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except RequestException as error:
        return {"message": "во время выполнения запроса", "cod": error}
    except json.JSONDecodeError as error:
        return {"message": "во время разбора JSON", "cod": error}

    if data["cod"] == HTTPStatus.OK:
        dt = data["dt"]
        timezone = data["timezone"]
        name = data["name"]
        temperature = round(data["main"]["temp"] - settings.TO_CELSIUS)
        feels_like = round(data["main"]["feels_like"] - settings.TO_CELSIUS)
        weather = data["weather"][0]["description"]
        wind_speed = round(data["wind"]["speed"])
        cod = data["cod"]

        return {"dt": dt, "timezone": timezone, "city": name, "weather": weather, "temperature": temperature,
                "feels_like": feels_like, "wind_speed": wind_speed, "cod": cod}
    else:
        message = data["message"]
        cod = data["cod"]
        return {"message": message, "cod": cod}


def processing_data_weather(weather_data: dict):
    if weather_data["cod"] == HTTPStatus.OK:
        print_data_weather(weather_data)
        remembering_data_weather(weather_data)
    else:
        print(f"Ошибка: {weather_data['message']}. Код ошибки: {weather_data['cod']}")


def print_data_weather(weather_data_to_print: dict):
    timestamp = weather_data_to_print['dt']
    timezone = datetime.timezone(datetime.timedelta(seconds=weather_data_to_print['timezone']))
    dt_object = datetime.datetime.fromtimestamp(timestamp, timezone)
    print(f"\nТекущее время: {dt_object}")
    print(f"Название города: {weather_data_to_print['city']}")
    print(f"Погодные условия: {weather_data_to_print['weather']}")
    print(f"Текущая температура: {weather_data_to_print['temperature']} градусов по цельсию")
    print(f"Ощущается как: {weather_data_to_print['feels_like']} градусов по цельсию")
    print(f"Скорость ветра: {weather_data_to_print['wind_speed']} м/с\n")


def remembering_data_weather(weather_data_to_history: dict):
    try:
        with open("request_weather_history.json", "r") as json_file:
            existing_data = json.load(json_file)
        existing_data[str(len(existing_data) + 1)] = weather_data_to_history
        with open("request_weather_history.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Ошибка при чтении файла: {error}")


def print_certain_weather_request(request_number: str):
    with open("request_weather_history.json", "r") as json_file:
        all_weather_data = json.load(json_file)
    try:
        weather_data = all_weather_data[str(request_number)]
        print_data_weather(weather_data)
    except KeyError as error:
        print(f"\n!!! Записи {error} нет !!! Всего {get_number_of_request()} ")


def print_last_n_weather_request(count_of_records: int):
    with open("request_weather_history.json", "r") as json_file:
        all_weather_data = json.load(json_file)
    try:
        for i in range(len(all_weather_data) - count_of_records + 1, len(all_weather_data) + 1):
            weather_data = all_weather_data[str(i)]
            print_data_weather(weather_data)
    except KeyError:
        print(f"\n!!! Ошибка. {count_of_records} такого количества записей нет !!! Всего {get_number_of_request()} ")
        for i in range(1, len(all_weather_data) + 1):
            weather_data = all_weather_data[str(i)]
            print_data_weather(weather_data)


def get_number_of_request() -> int:
    with open("request_weather_history.json", "r") as json_file:
        weather_data = json.load(json_file)
    return len(weather_data)


def delete_request_history():
    empty_dictionary = {}
    with open("request_weather_history.json", "w") as json_file:
        json.dump(empty_dictionary, json_file)
    print("Все запросы из истории удалены")


def main():
    print("Варианты действий в приложении: 1 - Погода в моем местоположении, 2 - Погода в городе,"
          " 3 - История запросов, 4 - удаление всех запросов из истории, 5 - Выход")
    while True:
        match input("Введите действие (1, 2, 3, 4, 5): "):
            case "1":
                city = geocoder.ip('me').city
                processing_data_weather(get_weather_data(city))
            case "2":
                city = input("Введите город: ")
                processing_data_weather(get_weather_data(city))
            case "3":
                print("Варианты действий по истории запросов: 1 - Конкретную запись, 2 - n последних записей")
                while True:
                    match input("Введите действие (1, 2): "):
                        case "1":
                            record_number = input("Введите номер записи для вывода: ")
                            print_certain_weather_request(record_number)
                            break
                        case "2":
                            record_count = input("Введите сколько последних записей вывести: ")
                            try:
                                print_last_n_weather_request(int(record_count))
                                break
                            except ValueError:
                                print(f"\n!!! Ошибка. '{record_count}' не integer !!! ")
                        case _:
                            print("Некорректный ввод, попробуйте ещё раз")
            case "4":
                delete_request_history()
            case "5":
                print("Выход из программы")
                break
            case _:
                print("Некорректный ввод, попробуйте ещё раз")


if __name__ == "__main__":
    main()
