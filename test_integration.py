import pytest
from unittest.mock import patch
from src.main import fetch_and_store_weather

API_KEY = "fake-key"

def test_successful_flow():
    with patch("src.main.get_weather") as mock_get_weather, \
         patch("src.main.insert_weather") as mock_insert_weather:  # Мокаем insert_weather
        mock_get_weather.return_value = {
            "city": "Paris",
            "region": "Ile-de-France",
            "country": "France",
            "temperature": 15,
            "condition": "Cloudy"
        }
        result = fetch_and_store_weather("Paris", API_KEY)
        assert result is True
        mock_insert_weather.assert_called_once()  # Проверяем вызов insert_weather

def test_with_empty_city():
    with patch("src.main.get_weather") as mock_get_weather:
        mock_get_weather.return_value = {"error": "City name cannot be empty"}
        result = fetch_and_store_weather("", API_KEY)
        assert result is False

def test_with_negative_temperature():
    with patch("src.main.get_weather") as mock_get_weather, \
         patch("src.main.insert_weather") as mock_insert_weather:  # Мокаем insert_weather
        mock_get_weather.return_value = {
            "city": "Murmansk",
            "region": "Murmansk Oblast",
            "country": "Russia",
            "temperature": -25,
            "condition": "Snow"
        }
        result = fetch_and_store_weather("Murmansk", API_KEY)
        assert result is True
        mock_insert_weather.assert_called_once()  # Проверяем вызов insert_weather

def test_exception_handling():
    with patch("src.main.get_weather", side_effect=Exception("API crashed")):
        result = fetch_and_store_weather("Berlin", API_KEY)
        assert result is False
