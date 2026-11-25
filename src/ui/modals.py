from __future__ import annotations

from tkinter.font import BOLD
from typing import Callable

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.core.command_router import CommandRouter
from src.services.user_config_service import UserConfig, UserConfigService
from src.services.weather_service import WeatherService


class AddCommandDialog(ctk.CTkToplevel):
    """Modal para adicionar e remover comandos personalizados de voz."""

    ACTION_TYPES = {
        "Abrir site (ex: https://github.com)": "web!:",
        "Pesquisar no site (use * na frase)": "web?:",
        "Abrir programa (ex: calc.exe)": "path:",
    }

    def __init__(
        self,
        master: ctk.CTk,
        router: CommandRouter,
        on_changed: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master)
        self.router = router
        self.on_changed = on_changed
        self.title("Gerenciar Comandos")
        self.geometry("560x500")
        self.resizable(False, False)
        self.configure(fg_color="#0f172a")
        self.transient(master)
        self.grab_set()
        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Adicionar Novo Comando",
            font=("Roboto", 20, BOLD),
            text_color="#f8fafc",
        ).grid(row=0, column=0, padx=24, pady=(20, 4), sticky="w")

        ctk.CTkLabel(
            self,
            text='Use "*" na frase se o comando receber um termo (ex.: "buscar no github *").',
            font=("Roboto", 12),
            text_color="#94a3b8",
        ).grid(row=1, column=0, padx=24, pady=(0, 12), sticky="w")

        form = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        form.grid(row=2, column=0, padx=24, pady=(0, 14), sticky="ew")
        form.grid_columnconfigure(0, weight=1)

        self.phrase_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text='Frase de voz (ex.: "abrir github")',
            fg_color="#0f172a",
            border_color="#334155",
        )
        self.phrase_entry.grid(row=0, column=0, padx=16, pady=(14, 8), sticky="ew")

        self.type_menu = ctk.CTkOptionMenu(
            form,
            height=36,
            values=list(self.ACTION_TYPES.keys()),
            fg_color="#0f172a",
            button_color="#0284c7",
        )
        self.type_menu.grid(row=1, column=0, padx=16, pady=6, sticky="ew")

        self.target_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text="URL ou programa (ex.: https://github.com ou https://site.com/search?q={query})",
            fg_color="#0f172a",
            border_color="#334155",
        )
        self.target_entry.grid(row=2, column=0, padx=16, pady=6, sticky="ew")

        ctk.CTkButton(
            form,
            height=38,
            text="Salvar comando",
            font=("Roboto", 14, BOLD),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self._save_command,
        ).grid(row=3, column=0, padx=16, pady=(8, 14), sticky="ew")

        ctk.CTkLabel(
            self,
            text="Seus comandos personalizados",
            font=("Roboto", 14, BOLD),
            text_color="#cbd5e1",
        ).grid(row=3, column=0, padx=24, pady=(4, 6), sticky="w")

        self.list_frame = ctk.CTkScrollableFrame(self, height=150, fg_color="#1e293b")
        self.list_frame.grid(row=4, column=0, padx=24, pady=(0, 18), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

    def _save_command(self) -> None:
        phrase = self.phrase_entry.get().strip()
        target = self.target_entry.get().strip()
        prefix = self.ACTION_TYPES[self.type_menu.get()]

        if not phrase or not target:
            CTkMessagebox(
                title="Comando",
                message="Preencha a frase de voz e o destino.",
                icon="cancel",
                option_1="OK",
            )
            return

        if prefix == "web?:" and "*" not in phrase:
            CTkMessagebox(
                title="Comando",
                message='Comandos de pesquisa precisam conter "*" na frase.',
                icon="warning",
                option_1="OK",
            )
            return

        self.router.add_user_command(phrase, f"{prefix}{target}")
        self.phrase_entry.delete(0, "end")
        self.target_entry.delete(0, "end")
        self._refresh_list()
        if self.on_changed is not None:
            self.on_changed()

    def _remove_command(self, phrase: str) -> None:
        self.router.remove_user_command(phrase)
        self._refresh_list()
        if self.on_changed is not None:
            self.on_changed()

    def _refresh_list(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = self.router.list_user_commands()
        if not items:
            ctk.CTkLabel(
                self.list_frame,
                text="Nenhum comando personalizado cadastrado ainda.",
                font=("Roboto", 12),
                text_color="#94a3b8",
            ).grid(row=0, column=0, padx=10, pady=12, sticky="w")
            return

        for idx, entry in enumerate(items):
            phrase, action = next(iter(entry.items()))
            row = ctk.CTkFrame(self.list_frame, fg_color="#0f172a", corner_radius=8)
            row.grid(row=idx, column=0, padx=6, pady=4, sticky="ew")
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row,
                text=f'"{phrase}" → {action}',
                font=("Roboto", 12),
                text_color="#e2e8f0",
                anchor="w",
            ).grid(row=0, column=0, padx=10, pady=6, sticky="ew")

            ctk.CTkButton(
                row,
                width=70,
                height=26,
                text="Excluir",
                fg_color="#b91c1c",
                hover_color="#991b1b",
                font=("Roboto", 11, BOLD),
                command=lambda p=phrase: self._remove_command(p),
            ).grid(row=0, column=1, padx=8, pady=6)


class SettingsDialog(ctk.CTkToplevel):
    """Modal para configurar API Key do OpenWeatherMap, cidade e velocidade da voz."""

    def __init__(
        self,
        master: ctk.CTk,
        config_service: UserConfigService,
        weather_service: WeatherService,
        on_saved: Callable[[UserConfig], None],
    ) -> None:
        super().__init__(master)
        self.config_service = config_service
        self.weather_service = weather_service
        self.on_saved = on_saved
        self.current = self.config_service.load()

        self.title("Configurações da Liza")
        self.geometry("500x410")
        self.resizable(False, False)
        self.configure(fg_color="#0f172a")
        self.transient(master)
        self.grab_set()
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Configurações de API e Voz",
            font=("Roboto", 20, BOLD),
            text_color="#f8fafc",
        ).grid(row=0, column=0, padx=24, pady=(20, 12), sticky="w")

        card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        card.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="OpenWeatherMap API Key (Clima)",
            font=("Roboto", 13, BOLD),
            text_color="#cbd5e1",
        ).grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")

        self.api_key_entry = ctk.CTkEntry(
            card,
            height=38,
            placeholder_text="Cole sua API Key aqui",
            fg_color="#0f172a",
            border_color="#334155",
            show="*",
        )
        self.api_key_entry.insert(0, self.current.openweather_api_key)
        self.api_key_entry.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(
            card,
            text="Cidade padrão (ex.: Salvador,BR)",
            font=("Roboto", 13, BOLD),
            text_color="#cbd5e1",
        ).grid(row=2, column=0, padx=16, pady=(4, 4), sticky="w")

        self.city_entry = ctk.CTkEntry(
            card,
            height=38,
            placeholder_text="Salvador,BR",
            fg_color="#0f172a",
            border_color="#334155",
        )
        self.city_entry.insert(0, self.current.weather_city)
        self.city_entry.grid(row=3, column=0, padx=16, pady=(0, 12), sticky="ew")

        self.rate_label = ctk.CTkLabel(
            card,
            text=f"Velocidade da voz: {self.current.tts_rate}",
            font=("Roboto", 13, BOLD),
            text_color="#cbd5e1",
        )
        self.rate_label.grid(row=4, column=0, padx=16, pady=(4, 4), sticky="w")

        self.rate_slider = ctk.CTkSlider(
            card,
            from_=120,
            to=260,
            number_of_steps=14,
            command=self._on_rate_change,
        )
        self.rate_slider.set(self.current.tts_rate)
        self.rate_slider.grid(row=5, column=0, padx=16, pady=(0, 12), sticky="ew")

        self.test_status_label = ctk.CTkLabel(
            card,
            text="",
            font=("Roboto", 12),
            text_color="#94a3b8",
        )
        self.test_status_label.grid(row=6, column=0, padx=16, pady=(0, 12), sticky="w")

        actions_row = ctk.CTkFrame(self, fg_color="transparent")
        actions_row.grid(row=2, column=0, padx=24, pady=(0, 20), sticky="ew")
        actions_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            actions_row,
            height=40,
            text="Testar API Key",
            fg_color="#334155",
            hover_color="#475569",
            command=self._test_api,
        ).grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(
            actions_row,
            height=40,
            text="Salvar configurações",
            font=("Roboto", 14, BOLD),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self._save,
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def _on_rate_change(self, value: float) -> None:
        self.rate_label.configure(text=f"Velocidade da voz: {int(round(value))}")

    def _test_api(self) -> None:
        ok, message = self.weather_service.test_connection(
            self.api_key_entry.get(), self.city_entry.get()
        )
        color = "#22c55e" if ok else "#f87171"
        self.test_status_label.configure(text=message, text_color=color)

    def _save(self) -> None:
        updated = self.config_service.save(
            UserConfig(
                openweather_api_key=self.api_key_entry.get(),
                weather_city=self.city_entry.get(),
                tts_rate=int(round(self.rate_slider.get())),
            )
        )
        self.on_saved(updated)
        self.destroy()
