from __future__ import annotations

import logging

import customtkinter as ctk

from src.config.settings import Settings
from src.core.actions import ActionExecutor
from src.core.command_router import CommandRouter
from src.core.speech import SpeechEngine
from src.domain.usuario import Usuario
from src.services.auth_service import AuthService
from src.services.session_service import SessionService
from src.services.user_config_service import UserConfigService
from src.services.weather_service import WeatherService
from src.ui.home_frame import HomeFrame
from src.ui.login_frame import LoginFrame

try:
    import keyboard
except ImportError:
    keyboard = None

logger = logging.getLogger(__name__)


class LizaApp(ctk.CTk):
    """Janela principal da aplicação Liza (1200x620)."""

    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.settings = settings or Settings.from_env()
        self.user_config_service = UserConfigService(self.settings)
        self.user_config = self.user_config_service.load()

        self.auth_service = AuthService(self.settings)
        self.session_service = SessionService()
        self.weather_service = WeatherService(self.settings)
        self.weather_service.configure(
            self.user_config.openweather_api_key, self.user_config.weather_city
        )

        self.router = CommandRouter()
        self.executor = ActionExecutor(self.router, self.weather_service)
        self._speech: SpeechEngine | None = None
        self._hotkey_registered = False

        self.title("Liza")
        self.geometry("1200x620")
        self.minsize(1000, 560)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._current_frame: ctk.CTkFrame | None = None
        saved_user = self.session_service.load()
        if saved_user is not None:
            self._show_home(saved_user)
        else:
            self._show_login()

    def _set_frame(self, frame: ctk.CTkFrame) -> None:
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = frame
        self._current_frame.grid(row=0, column=0, sticky="nsew")

    def _show_login(self) -> None:
        self._unregister_hotkey()
        self.unbind("<F1>")
        self._set_frame(
            LoginFrame(
                self,
                self.auth_service,
                self.settings.db_backend,
                self._on_login_success,
            )
        )

    def _on_login_success(self, usuario: Usuario, remember: bool) -> None:
        if remember:
            self.session_service.save(usuario)
        else:
            self.session_service.clear()
        self._show_home(usuario)

    def _show_home(self, usuario: Usuario) -> None:
        if self._speech is None:
            self._speech = SpeechEngine(tts_rate=self.user_config.tts_rate)
        home = HomeFrame(
            self,
            usuario,
            self._speech,
            self.router,
            self.executor,
            self.user_config_service,
            self.weather_service,
            on_logout=self._logout,
        )
        self._set_frame(home)
        self.bind("<F1>", lambda _event: home.start_listening())
        self._register_global_hotkey(home)

    def _register_global_hotkey(self, home: HomeFrame) -> None:
        self._unregister_hotkey()
        if keyboard is None:
            return
        try:
            keyboard.add_hotkey("f1", lambda: self.after(0, home.start_listening))
            self._hotkey_registered = True
        except Exception:
            logger.warning("Não foi possível registrar hotkey global F1; usando atalho local.")

    def _unregister_hotkey(self) -> None:
        if keyboard is not None and self._hotkey_registered:
            try:
                keyboard.remove_hotkey("f1")
            except Exception:
                pass
            self._hotkey_registered = False

    def _logout(self) -> None:
        self.session_service.clear()
        self._show_login()

    def _on_close(self) -> None:
        self._unregister_hotkey()
        self.destroy()
