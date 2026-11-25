from __future__ import annotations

from tkinter.font import BOLD
from typing import Callable

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

from src.config.settings import resource_path
from src.domain.usuario import Usuario
from src.services.auth_service import AuthError, AuthService


class LoginFrame(ctk.CTkFrame):
    """Tela de login e cadastro local alinhada ao protótipo (Figura 1)."""

    def __init__(
        self,
        master: ctk.CTk,
        auth_service: AuthService,
        db_backend: str,
        on_login_success: Callable[[Usuario, bool], None],
    ) -> None:
        super().__init__(master, fg_color="#0f172a")
        self.auth_service = auth_service
        self.db_backend = db_backend
        self.on_login_success = on_login_success
        self._is_register_mode = False
        self._logo_image = self._load_logo()
        self._build_ui()

    @staticmethod
    def _load_logo() -> ctk.CTkImage | None:
        logo_path = resource_path("assets/liza.png")
        if not logo_path.exists():
            return None
        return ctk.CTkImage(Image.open(logo_path), size=(150, 150))

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkFrame(self, fg_color="#0b1120", corner_radius=0)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_rowconfigure(5, weight=1)

        if self._logo_image is not None:
            ctk.CTkLabel(left_panel, text="", image=self._logo_image).grid(
                row=1, column=0, padx=40, pady=(20, 8)
            )

        ctk.CTkLabel(
            left_panel,
            text="L I Z A",
            font=("Roboto", 22, BOLD),
            text_color="#e2e8f0",
        ).grid(row=2, column=0, padx=40, pady=(0, 36))

        ctk.CTkLabel(
            left_panel,
            text="Sua assistente pessoal\npara tornar o dia mais simples.",
            font=("Roboto", 20, BOLD),
            text_color="#f8fafc",
            justify="center",
        ).grid(row=3, column=0, padx=40, pady=(0, 10))

        ctk.CTkLabel(
            left_panel,
            text="Pesquise, organize e controle tudo por voz.",
            font=("Roboto", 13),
            text_color="#94a3b8",
        ).grid(row=4, column=0, padx=40, pady=(0, 20))

        right_panel = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(2, weight=1)

        card = ctk.CTkFrame(
            right_panel,
            fg_color="#1e293b",
            corner_radius=14,
            border_width=1,
            border_color="#334155",
        )
        card.grid(row=1, column=0, padx=48, pady=32, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="ACESSO LOCAL" if self.db_backend == "sqlite" else "ACESSO NUVEM",
            font=("Roboto", 11, BOLD),
            text_color="#38bdf8",
        ).grid(row=0, column=0, padx=28, pady=(24, 2), sticky="w")

        self.form_title = ctk.CTkLabel(
            card,
            text="Bem-vindo de volta",
            font=("Roboto", 24, BOLD),
            text_color="#f8fafc",
        )
        self.form_title.grid(row=1, column=0, padx=28, pady=(0, 4), sticky="w")

        self.form_subtitle = ctk.CTkLabel(
            card,
            text="Entre para ativar sua experiência com a Liza.",
            font=("Roboto", 13),
            text_color="#94a3b8",
        )
        self.form_subtitle.grid(row=2, column=0, padx=28, pady=(0, 16), sticky="w")

        self.nome_entry = ctk.CTkEntry(
            card,
            height=40,
            placeholder_text="Nome completo",
            font=("Roboto", 14),
            fg_color="#0f172a",
            border_color="#334155",
        )

        self.email_entry = ctk.CTkEntry(
            card,
            height=40,
            placeholder_text="E-mail",
            font=("Roboto", 14),
            fg_color="#0f172a",
            border_color="#334155",
        )
        self.email_entry.grid(row=4, column=0, padx=28, pady=6, sticky="ew")

        self.senha_entry = ctk.CTkEntry(
            card,
            height=40,
            placeholder_text="Senha",
            font=("Roboto", 14),
            fg_color="#0f172a",
            border_color="#334155",
            show="*",
        )
        self.senha_entry.grid(row=5, column=0, padx=28, pady=6, sticky="ew")
        self.senha_entry.bind("<Return>", lambda _event: self._submit())

        self.remember_var = ctk.BooleanVar(value=True)
        self.remember_checkbox = ctk.CTkCheckBox(
            card,
            text="Manter conectado",
            variable=self.remember_var,
            font=("Roboto", 13),
            text_color="#cbd5e1",
        )
        self.remember_checkbox.grid(row=6, column=0, padx=28, pady=(8, 4), sticky="w")

        self.submit_btn = ctk.CTkButton(
            card,
            height=42,
            text="Entrar na Liza",
            font=("Roboto", 15, BOLD),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self._submit,
        )
        self.submit_btn.grid(row=7, column=0, padx=28, pady=(12, 8), sticky="ew")

        self.toggle_btn = ctk.CTkButton(
            card,
            height=34,
            text="Criar nova conta",
            fg_color="transparent",
            border_width=1,
            border_color="#334155",
            text_color="#cbd5e1",
            font=("Roboto", 13),
            command=self._toggle_mode,
        )
        self.toggle_btn.grid(row=8, column=0, padx=28, pady=(0, 12), sticky="ew")

        db_status = (
            "Banco de testes local ativo"
            if self.db_backend == "sqlite"
            else "Banco MySQL configurado"
        )
        ctk.CTkLabel(
            card,
            text=db_status,
            font=("Roboto", 11),
            text_color="#64748b",
        ).grid(row=9, column=0, padx=28, pady=(0, 18), sticky="w")

    def _toggle_mode(self) -> None:
        self._is_register_mode = not self._is_register_mode
        if self._is_register_mode:
            self.form_title.configure(text="Criar conta")
            self.form_subtitle.configure(text="Cadastre-se localmente para usar a Liza.")
            self.nome_entry.grid(row=3, column=0, padx=28, pady=6, sticky="ew")
            self.submit_btn.configure(text="Cadastrar e Entrar")
            self.toggle_btn.configure(text="Já tenho conta")
        else:
            self.form_title.configure(text="Bem-vindo de volta")
            self.form_subtitle.configure(text="Entre para ativar sua experiência com a Liza.")
            self.nome_entry.grid_forget()
            self.submit_btn.configure(text="Entrar na Liza")
            self.toggle_btn.configure(text="Criar nova conta")

    def _submit(self) -> None:
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get()
        remember = self.remember_var.get()

        if self._is_register_mode:
            nome = self.nome_entry.get().strip()
            try:
                usuario = self.auth_service.registrar(email=email, senha=senha, nome=nome)
            except AuthError as exc:
                CTkMessagebox(title="Cadastro", message=str(exc), icon="cancel", option_1="OK")
                return
            CTkMessagebox(
                title="Cadastro",
                message="Conta criada com sucesso!",
                icon="check",
                option_1="OK",
            )
            self.on_login_success(usuario, remember)
            return

        try:
            usuario = self.auth_service.autenticar(email=email, senha=senha)
        except AuthError as exc:
            CTkMessagebox(title="Erro", message=str(exc), icon="cancel", option_1="OK")
            return

        if usuario is None:
            CTkMessagebox(
                title="Login",
                message="E-mail ou senha incorretos.",
                icon="cancel",
                option_1="OK",
            )
            return

        self.on_login_success(usuario, remember)
