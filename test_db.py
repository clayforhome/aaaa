from src.db import get_connection

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Успешное подключение к БД через PyMySQL")
        conn.close()
    except Exception as e:
        print("❌ Ошибка при подключении:", e)
