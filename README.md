# Weather_App

Консольное приложение Weather_App предназначено для получения информации о погоде в определенном городе или на основе местоположения пользователя, а также для хранения истории запросов пользователя. Информация будет выводиться в заданном формате:

```
Текущее время: 2023-10-03 09:48:47+03:00
Название города: Санкт-Петербург
Погодные условия: облачно
Текущая температура: 12 градусов по цельсию
Ощущается как: 11 градусов по цельсию
Скорость ветра: 5 м/c
```

### Реализация приложения
1. Для разработки приложения используется язык программирования Python
2. Данные о погоде берутся через API OpenWeatherMap с использованием библиотеки Requests, отправляя запросы API о погоде в конкретном городе
3. Для определения местоположения пользователя планируется использовать библиотеку Geocoder, которая позволяет получить IP-адрес, координаты (широту и долготу) пользователя и соответственно город по этим данным. Затем полученная информация передается в API OpenWeatherMap для получения необходимых данных о погоде
4. История запросов пользователя будет храниться в формате JSON. Файл истории запросов и последующая работа с ним будут осуществляться с использованием модуля JSON
5. Взаимодействие с программой планируется осуществлять через консоль. Доступные команды: "1" - для получения информации о погоде в определенном городе, "2" - для получения информации о погоде в текущем месте, "3" - для получения истории прошлых запросов, "4" - для удаления истории запросов, "5" - для выхода из программы
6. Обработка невалидных запросов будет происходить следующим образом: сначала проверяется код ответа, если он равен 200, всё хорошо, при ином значении выводится код ошибки, проверяется наличие поля "message" в JSON-ответе и выводится содержимое этого сообщение, если оно есть

### Установка ПО для работы приложения
1. Установить интерпретатор python версии 3.11 или выше.
2. В папке с файлами приложения создать виртуальное окружение с помощью консольной команды `python -m venv {venv name}`, после чего активировать его командой `venv\Scripts\activate.bat` для Windows или `source venv/bin/activate` для Linux и MacOS.
3. Установить требуемые библиотеки в активированное виртуальное окружение командой `pip install -r requirements.txt`
4. Для запуска приложения введите команду `python main.py`
