from src.config.settings import Settings
from src.services.user_config_service import UserConfig, UserConfigService


def _settings(tmp_path) -> Settings:
    return Settings(
        db_backend="sqlite",
        sqlite_path=tmp_path / "app.db",
        db_host="localhost",
        db_user="root",
        db_password="",
        db_name="liza",
        openweather_api_key="env-key",
        weather_city="Salvador,BR",
    )


def test_load_defaults_and_save_overrides(tmp_path):
    service = UserConfigService(_settings(tmp_path), tmp_path / "user_config.json")
    initial = service.load()
    assert initial.openweather_api_key == "env-key"
    assert initial.weather_city == "Salvador,BR"
    assert initial.tts_rate == 180

    service.save(UserConfig(openweather_api_key="ui-key", weather_city="Recife,BR", tts_rate=220))
    reloaded = service.load()
    assert reloaded.openweather_api_key == "ui-key"
    assert reloaded.weather_city == "Recife,BR"
    assert reloaded.tts_rate == 220
