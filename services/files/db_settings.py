
NAME_DATABASE = 'weather_app_data.db'
NAME_TABLE = 'weather_request_data'

CREATE_DATABASE_REQUEST = '''
    CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        city_name TEXT,
        weather_conditions TEXT,
        temperature INT,
        temperature_feels_like INT,
        wind_speed INT
    )
'''

DELETE_FROM_REQUEST = '''
    DELETE FROM {}
'''

REFRESH_ID = '''
    DELETE FROM sqlite_sequence
'''

INSERT_REQUEST_INTO_TABLE = '''
    INSERT INTO {}
    (id, date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed)
    VALUES (?, ?, ?, ?, ?, ?, ?)
'''

SELECT_N_LAST_REQUEST = '''
    SELECT
    id, date, city_name, weather_conditions, temperature, temperature_feels_like, wind_speed
    FROM {}
    ORDER BY id DESC LIMIT {}
'''
