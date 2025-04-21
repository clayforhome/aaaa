# Проект: Погода + База Данных (Python + MySQL)

## Как запустить:
1. Установить зависимости:
   pip install requests pymysql

2. Установить API-ключ:
   - Либо добавить в переменные среды `WEATHERAPI_KEY`
   - Либо ввести вручную при запуске

3. Настроить подключение к БД в `db.py`:
   ```python
   return pymysql.connect(
       host="localhost",
       user="root",
       password="----",
       database="weather_db", 
       charset="utf8mb4",
       cursorclass=pymysql.cursors.Cursor
   )

4. Запустить проект введя в терминал:
   python main.py

## Тесты:
1. Все тесты запускаются отдельно от файла main.py используя:
   python пример_название_теста.py
