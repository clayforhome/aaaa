import pymysql.cursors

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="123456789",
        database="weather_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_weather(data: dict):
    """
    Вставляет или обновляет запись о погоде в БД.
    Используется функцией fetch_and_store_weather.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Найти или вставить город
    cursor.execute(
        "SELECT id FROM cities WHERE name=%s AND region=%s AND country=%s",
        (data['city'], data['region'], data['country'])
    )
    row = cursor.fetchone()
    if row:
        city_id = row["id"]
    else:
        cursor.execute(
            "INSERT INTO cities (name, region, country) VALUES (%s, %s, %s)",
            (data['city'], data['region'], data['country'])
        )
        city_id = cursor.lastrowid

    # Обновить или вставить погоду
    cursor.execute("SELECT id FROM weather WHERE city_id=%s", (city_id,))
    if cursor.fetchone():
        cursor.execute(
            "UPDATE weather SET temperature=%s, `condition`=%s, updated_at=NOW() "
            "WHERE city_id=%s",
            (data['temperature'], data['condition'], city_id)
        )
    else:
        cursor.execute(
            "INSERT INTO weather (city_id, temperature, `condition`, updated_at) "
            "VALUES (%s, %s, %s, NOW())",
            (city_id, data['temperature'], data['condition'])
        )

    conn.commit()
    cursor.close()
    conn.close()
