from __future__ import annotations

import threading
from tkinter.font import BOLD
from typing import Callable

import customtkinter as ctk
from PIL import Image

from src.config.settings import resource_path
from src.core.actions import ActionExecutor
from src.core.command_router import CommandRouter
from src.core.speech import SpeechEngine
from src.domain.usuario import Usuario

try:
    import winsound
except ImportError:
    winsound = None


class HomeFrame(ctk.CTkFrame):
    """Tela principal da assistente Liza alinhada ao protótipo (Figura 2)."""

    COMMAND_EXAMPLES = (
        '• "Pesquise por <assunto>" (Google)',
        '• "Pesquise vídeos de <tema>" (YouTube)',
        '• "Encontre referências sobre <tema>" (Wikipedia)',
        '• "Encontre músicas de <artista>" (Spotify)',
        '• "Qual o clima hoje" / "Abrir calculadora" / "Ajuda"',
    )

    def __init__(
        self,
        master: ctk.CTk,
        usuario: Usuario,
        speech: SpeechEngine,
        router: CommandRouter,
        executor: ActionExecutor,
        on_logout: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color="#0f172a")
        self.usuario = usuario
        self.speech = speech
        self.router = router
        self.executor = executor
        self.on_logout = on_logout
        self._listening = False
        self._logo_image = self._load_logo()
        self._build_ui()

    @staticmethod
    def _load_logo() -> ctk.CTkImage | None:
        logo_path = resource_path("assets/liza.png")
        if not logo_path.exists():
            return None
        return ctk.CTkImage(Image.open(logo_path), size=(72, 72))

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=0, minsize=220)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(self, width=220, fg_color="#0b1120", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)
        sidebar.grid_columnconfigure(0, weight=1)

        if self._logo_image is not None:
            ctk.CTkLabel(sidebar, text="", image=self._logo_image).grid(
                row=0, column=0, padx=24, pady=(28, 6)
            )

        ctk.CTkLabel(
            sidebar,
            text="LIZA",
            font=("Roboto", 20, BOLD),
            text_color="#e2e8f0",
        ).grid(row=1, column=0, padx=24, pady=(0, 12))

        ctk.CTkLabel(
            sidebar,
            text="● Sessão ativa",
            font=("Roboto", 13, BOLD),
            text_color="#22c55e",
        ).grid(row=2, column=0, padx=24, pady=(0, 4))

        ctk.CTkLabel(
            sidebar,
            text=self.usuario.nome,
            font=("Roboto", 13),
            text_color="#94a3b8",
            wraplength=180,
        ).grid(row=3, column=0, padx=20, pady=(0, 12))

        ctk.CTkButton(
            sidebar,
            text="Sair da conta",
            height=34,
            fg_color="transparent",
            border_width=1,
            border_color="#334155",
            text_color="#cbd5e1",
            command=self.on_logout,
        ).grid(row=5, column=0, padx=24, pady=24, sticky="ew")

        main_area = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        main_area.grid(row=0, column=1, padx=48, pady=36, sticky="nsew")
        main_area.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main_area,
            text="Sua Liza está pronta.",
            font=("Roboto", 30, BOLD),
            text_color="#f8fafc",
        ).grid(row=0, column=0, sticky="w", pady=(12, 4))

        ctk.CTkLabel(
            main_area,
            text="Diga o que você precisa e deixe a Liza cuidar do resto.",
            font=("Roboto", 15),
            text_color="#94a3b8",
        ).grid(row=1, column=0, sticky="w", pady=(0, 24))

        control_card = ctk.CTkFrame(
            main_area,
            fg_color="#1e293b",
            corner_radius=14,
            border_width=1,
            border_color="#334155",
        )
        control_card.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        control_card.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            control_card,
            text="Pronta para ouvir",
            font=("Roboto", 20, BOLD),
            text_color="#f8fafc",
        )
        self.status_label.grid(row=0, column=0, padx=28, pady=(24, 4), sticky="w")

        ctk.CTkLabel(
            control_card,
            text="Clique no botão ou pressione a tecla global F1 para começar.",
            font=("Roboto", 13),
            text_color="#94a3b8",
        ).grid(row=1, column=0, padx=28, pady=(0, 14), sticky="w")

        self.listen_btn = ctk.CTkButton(
            control_card,
            width=200,
            height=42,
            text="Ativar escuta",
            font=("Roboto", 15, BOLD),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.start_listening,
        )
        self.listen_btn.grid(row=2, column=0, padx=28, pady=(0, 14), sticky="w")

        self.transcript_label = ctk.CTkLabel(
            control_card,
            text="Último comando: —",
            font=("Roboto", 13),
            text_color="#cbd5e1",
            wraplength=760,
            justify="left",
        )
        self.transcript_label.grid(row=3, column=0, padx=28, pady=(0, 22), sticky="w")

        help_card = ctk.CTkFrame(
            main_area,
            fg_color="#111827",
            corner_radius=12,
            border_width=1,
            border_color="#1e293b",
        )
        help_card.grid(row=3, column=0, sticky="ew")
        help_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            help_card,
            text="Exemplos de comandos por voz",
            font=("Roboto", 14, BOLD),
            text_color="#38bdf8",
        ).grid(row=0, column=0, padx=20, pady=(14, 6), sticky="w")

        ctk.CTkLabel(
            help_card,
            text="\n".join(self.COMMAND_EXAMPLES),
            font=("Roboto", 13),
            text_color="#94a3b8",
            justify="left",
        ).grid(row=1, column=0, padx=20, pady=(0, 14), sticky="w")

    def _play_beep(self) -> None:
        bip_path = resource_path("assets/bip.wav")
        if winsound is not None and bip_path.exists():
            try:
                winsound.PlaySound(str(bip_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            except RuntimeError:
                pass

    def start_listening(self) -> None:
        if self._listening:
            return
        self._listening = True
        self.listen_btn.configure(state="disabled", text="Ouvindo...")
        self.status_label.configure(text="Ouvindo...")
        self._play_beep()
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self) -> None:
        result = self.speech.listen()
        if result.error_message:
            self.after(0, lambda: self._finish_listening("Pronta para ouvir", result.error_message))
            self.speech.speak(result.error_message)
            return

        match = self.router.match(result.text)
        if match is None:
            feedback = "Não consegui entender o comando."
            self.after(
                0,
                lambda: self._finish_listening(
                    "Comando não reconhecido", f'Último comando: "{result.text}"'
                ),
            )
            self.speech.speak(feedback)
            return

        response_text = self.executor.execute(match)
        self.after(
            0,
            lambda: self._finish_listening(
                "Pronta para ouvir", f'Último comando: "{result.text}" → {response_text}'
            ),
        )
        self.speech.speak(response_text)

    def _finish_listening(self, status_text: str, transcript_text: str) -> None:
        if not self.winfo_exists():
            return
        self._listening = False
        self.listen_btn.configure(state="normal", text="Ativar escuta")
        self.status_label.configure(text=status_text)
        self.transcript_label.configure(text=transcript_text)
