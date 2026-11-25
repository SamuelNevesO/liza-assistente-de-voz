from unittest.mock import MagicMock

from src.config.settings import Settings
from src.core.actions import ActionExecutor
from src.core.command_router import CommandMatch, CommandRouter
from src.services.weather_service import WeatherService


def _make_settings(tmp_path, api_key="fake-key") -> Settings:
    return Settings(
        db_backend="sqlite",
        sqlite_path=tmp_path / "test.db",
        db_host="localhost",
        db_user="root",
        db_password="",
        db_name="liza",
        openweather_api_key=api_key,
        weather_city="Salvador,BR",
    )


def test_build_search_url_encodes_special_chars():
    url = ActionExecutor.build_search_url(
        "https://www.google.com/search?q={query}", "café & código"
    )
    assert url == "https://www.google.com/search?q=caf%C3%A9+%26+c%C3%B3digo"


def test_execute_weather_uses_weather_service(tmp_path, monkeypatch):
    settings = _make_settings(tmp_path)
    weather = WeatherService(settings)
    monkeypatch.setattr(weather, "get_temperature", MagicMock(return_value=28))
    executor = ActionExecutor(CommandRouter(), weather)

    feedback = executor.execute(CommandMatch(section="abrir", action="temp"))
    assert "28 graus Celsius" in feedback


def test_execute_web_search_opens_browser(tmp_path, monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr("src.core.actions.webbrowser.open_new", opened.append)

    executor = ActionExecutor(CommandRouter(), WeatherService(_make_settings(tmp_path)))
    feedback = executor.execute(
        CommandMatch(
            section="abrir",
            action="web?:https://pt.wikipedia.org/w/index.php?search={query}",
            argument="inteligência artificial",
        )
    )
    assert len(opened) == 1
    assert "pt.wikipedia.org/w/index.php?search=intelig%C3%AAncia+artificial" in opened[0]
    assert "Pesquisando inteligência artificial" == feedback


def test_execute_help_and_reload_and_program(tmp_path, monkeypatch):
    launched: list[list[str]] = []
    monkeypatch.setattr("src.core.actions.subprocess.Popen", launched.append)
    executor = ActionExecutor(CommandRouter(), WeatherService(_make_settings(tmp_path)))

    help_msg = executor.execute(CommandMatch(section="abrir", action="help"))
    assert "Google" in help_msg

    reload_msg = executor.execute(CommandMatch(section="abrir", action="commands"))
    assert "atualizados" in reload_msg.lower()

    prog_msg = executor.execute(CommandMatch(section="abrir", action="path:calc.exe"))
    assert launched == [["calc.exe"]]
    assert "calc" in prog_msg.lower()
