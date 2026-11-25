from unittest.mock import MagicMock

import requests

from src.config.settings import Settings
from src.services.weather_service import WeatherService


def _settings(tmp_path, api_key="key-123") -> Settings:
    return Settings(
        db_backend="sqlite",
        sqlite_path=tmp_path / "w.db",
        db_host="localhost",
        db_user="root",
        db_password="",
        db_name="liza",
        openweather_api_key=api_key,
        weather_city="Salvador,BR",
    )


def test_get_temperature_returns_rounded_int(tmp_path, monkeypatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"main": {"temp": 27.6}}
    mock_resp.raise_for_status.return_value = None
    monkeypatch.setattr("src.services.weather_service.requests.get", MagicMock(return_value=mock_resp))

    service = WeatherService(_settings(tmp_path))
    assert service.get_temperature() == 28


def test_get_temperature_without_api_key_returns_none(tmp_path):
    service = WeatherService(_settings(tmp_path, api_key=""))
    assert service.get_temperature() is None


def test_get_temperature_handles_network_error(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "src.services.weather_service.requests.get",
        MagicMock(side_effect=requests.RequestException("offline")),
    )
    service = WeatherService(_settings(tmp_path))
    assert service.get_temperature() is None


def test_get_temperature_uses_ttl_cache(tmp_path, monkeypatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"main": {"temp": 25.2}}
    mock_resp.raise_for_status.return_value = None
    mock_get = MagicMock(return_value=mock_resp)
    monkeypatch.setattr("src.services.weather_service.requests.get", mock_get)

    service = WeatherService(_settings(tmp_path))
    assert service.get_temperature() == 25
    assert service.get_temperature() == 25
    assert mock_get.call_count == 1


def test_connection_reports_invalid_key(tmp_path, monkeypatch):
    mock_resp = MagicMock(status_code=401)
    monkeypatch.setattr("src.services.weather_service.requests.get", MagicMock(return_value=mock_resp))

    service = WeatherService(_settings(tmp_path))
    ok, msg = service.test_connection("bad-key", "Salvador,BR")
    assert ok is False
    assert "inválida" in msg.lower()
