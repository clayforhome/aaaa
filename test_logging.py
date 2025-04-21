import os
import tempfile
import logging
from unittest import mock
from src.main import fetch_and_store_weather

def test_logging_error_on_api_failure():
    test_city = "InvalidCity"
    test_api_key = "fake-key"

    with tempfile.NamedTemporaryFile(delete=False) as tmp_log:
        log_path = tmp_log.name

    logger = logging.getLogger("src.main")
    logger.setLevel(logging.ERROR)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with mock.patch("src.main.get_weather", return_value={"error": "город не найден"}):
        result = fetch_and_store_weather(test_city, test_api_key)
        assert result is False 

    with open(log_path, encoding="utf-8") as f:
        log_content = f.read()

    assert "город не найден" in log_content
    assert test_city in log_content

    # Закрываем обработчик перед удалением файла
    logger.removeHandler(handler)
    handler.close()
    os.remove(log_path)
