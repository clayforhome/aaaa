import requests
import logging

# Настройка логгера
logger = logging.getLogger("src.weather_api")
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler("error.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_weather(city: str, api_key: str) -> dict:
    """
    Получает погоду по названию города с использованием WeatherAPI.com.
    Возвращает словарь с данными или сообщением об ошибке.
    """
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            msg = data["error"].get("message", "Неизвестная ошибка API")
            logger.error(f"Ошибка API: {msg} (город: {city})")
            return {"error": msg}

        return {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"]
        }

    except requests.exceptions.HTTPError as http_err:
        msg = f"HTTP-ошибка: {http_err}"
        logger.error(f"{msg} (город: {city})")
        return {"error": msg}

    except requests.exceptions.RequestException as err:
        msg = f"Сетевая ошибка: {err}"
        logger.error(f"{msg} (город: {city})")
        return {"error": msg}
