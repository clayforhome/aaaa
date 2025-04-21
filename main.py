import os
import logging
from datetime import datetime
from weather_api import get_weather
from db import get_connection, insert_weather

# Настройка логгера
logger = logging.getLogger("src.main")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler("error.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

MENU = """
Выберите действие:
1 — Получить погоду и сохранить в БД
2 — Показать все записи
3 — Обновить запись погоды по городу
4 — Удалить запись по городу
5 — Поиск по городу
0 — Выход
> """

def save_weather_to_db(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Найти или вставить город
    cursor.execute(
        "SELECT id FROM cities WHERE name=%s AND region=%s AND country=%s",
        (data['city'], data['region'], data['country'])
    )
    row = cursor.fetchone()
    if row:
        city_id = row[0]
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
            "UPDATE weather "
            "SET temperature=%s, `condition`=%s, updated_at=%s "
            "WHERE city_id=%s",
            (data['temperature'], data['condition'], datetime.now(), city_id)
        )
    else:
        cursor.execute(
            "INSERT INTO weather (city_id, temperature, `condition`, updated_at) "
            "VALUES (%s, %s, %s, %s)",
            (city_id, data['temperature'], data['condition'], datetime.now())
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Данные сохранены/обновлены.")

def show_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT c.name, c.region, c.country, w.temperature, w.`condition`, w.updated_at "
        "FROM weather w JOIN cities c ON w.city_id=c.id"
    )
    for name, region, country, temp, cond, updated in cursor:
        print(f"{name}, {region or country}: {temp}°C, {cond} (обновлено: {updated})")
    cursor.close()
    conn.close()

def update_manual():
    city = input("Город для обновления: ").strip()
    temp = float(input("Новая температура: "))
    cond = input("Новое условие: ").strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE weather w "
        "JOIN cities c ON w.city_id=c.id "
        "SET w.temperature=%s, w.`condition`=%s, w.updated_at=%s "
        "WHERE c.name=%s",
        (temp, cond, datetime.now(), city)
    )
    conn.commit()
    print(f"Обновлено строк: {cursor.rowcount}")
    cursor.close()
    conn.close()

def delete_city():
    city = input("Город для удаления: ").strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE w FROM weather w "
        "JOIN cities c ON w.city_id=c.id "
        "WHERE c.name=%s",
        (city,)
    )
    conn.commit()
    print(f"Удалено строк: {cursor.rowcount}")
    cursor.close()
    conn.close()

def search_city():
    city = input("Поиск (город): ").strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT c.name, w.temperature, w.`condition`, w.updated_at "
        "FROM weather w JOIN cities c ON w.city_id=c.id "
        "WHERE c.name LIKE %s",
        (f"%{city}%",)
    )
    for name, temp, cond, updated in cursor:
        print(f"{name}: {temp}°C, {cond} (обновлено: {updated})")
    cursor.close()
    conn.close()

# Функция для интеграционного теста
def fetch_and_store_weather(city: str, api_key: str) -> bool:
    """
    Получает погоду и сохраняет в БД.
    Возвращает True при успехе, False при ошибке.
    """
    if not city.strip():
        logger.error("Пустое имя города")
        return False

    try:
        data = get_weather(city, api_key)
        if "error" in data:
            logger.error(f"Ошибка получения погоды для {city}: {data['error']}")
            return False
        insert_weather(data)
        return True
    except Exception as e:
        logger.error(f"Исключение при обработке города {city}: {e}")
        return False

def main():
    api_key = os.getenv("WEATHERAPI_KEY") or input("Введите ваш API‑ключ: ").strip()

    while True:
        choice = input(MENU).strip()
        if choice == "1":
            city = input("Введите город (или город,страна): ").strip()
            success = fetch_and_store_weather(city, api_key)
            if not success:
                print("Не удалось получить или сохранить данные.")
        elif choice == "2":
            show_all()
        elif choice == "3":
            update_manual()
        elif choice == "4":
            delete_city()
        elif choice == "5":
            search_city()
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
