import pytest

from src.config.settings import Settings
from src.services.auth_service import AuthError, AuthService


def _make_settings(tmp_path) -> Settings:
    return Settings(
        db_backend="sqlite",
        sqlite_path=tmp_path / "liza_test.db",
        db_host="localhost",
        db_user="root",
        db_password="",
        db_name="liza",
        openweather_api_key="",
        weather_city="Salvador,BR",
    )


def test_register_and_authenticate_success(tmp_path):
    service = AuthService(_make_settings(tmp_path))
    created = service.registrar("Liza@Example.com", "segredo123", "Liza User")
    assert created.email == "liza@example.com"

    user = service.autenticar("liza@example.com", "segredo123")
    assert user is not None
    assert user.nome == "Liza User"


def test_authenticate_wrong_password_returns_none(tmp_path):
    service = AuthService(_make_settings(tmp_path))
    service.registrar("user@example.com", "correta", "User")
    assert service.autenticar("user@example.com", "errada") is None


def test_register_duplicate_email_raises(tmp_path):
    service = AuthService(_make_settings(tmp_path))
    service.registrar("dup@example.com", "1234", "User 1")
    with pytest.raises(AuthError):
        service.registrar("dup@example.com", "5678", "User 2")


def test_register_empty_fields_raises(tmp_path):
    service = AuthService(_make_settings(tmp_path))
    with pytest.raises(AuthError):
        service.registrar("", "1234", "User")


def test_authenticate_empty_or_unknown_returns_none(tmp_path):
    service = AuthService(_make_settings(tmp_path))
    assert service.autenticar("", "1234") is None
    assert service.autenticar("nobody@example.com", "1234") is None
