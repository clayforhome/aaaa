import pytest
from unittest.mock import patch, MagicMock
from src.weather_api import get_weather
from src.db import get_connection
import logging

def test_get_weather_valid_city(monkeypatch):
    sample_response = {
        "location": {
            "name": "Moscow",
            "region": "Moscow City",
            "country": "Russia"
        },
        "current": {
            "temp_c": 10.5,
            "condition": {"text": "Sunny"}
        }
    }

    mock_response = MagicMock()
    mock_response.json.return_value = sample_response
    mock_response.raise_for_status = lambda: None

    with patch("requests.get", return_value=mock_response):
        result = get_weather("Moscow", "fake-key")
        assert result["city"] == "Moscow"
        assert result["temperature"] == 10.5
        assert result["condition"] == "Sunny"

def test_get_weather_invalid_city():
    result = get_weather("InvalidCity", "fake-key")
    assert "error" in result

def test_get_weather_bad_type():
    result = get_weather(None, "fake-key")
    assert "error" in result

# Проверка подключения к базе
def test_db_connection():
    conn = get_connection()
    assert conn is not None
    assert conn.open  # conn.open == True, если соединение активно
    conn.close()

# Логгирование ошибки
def test_logging_error(tmp_path):
    log_file = tmp_path / "error.log"
    logger = logging.getLogger("weather_logger")
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler(log_file)
    logger.addHandler(handler)

    try:
        raise ValueError("Test error for logging")
    except ValueError as e:
        logger.error(f"Ошибка: {e}")

    with open(log_file) as f:
        contents = f.read()
    assert "Test error for logging" in contents
