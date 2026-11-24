from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Usuario:
    """Representa um usuário autenticado no sistema."""

    email: str
    nome: str
    data_nascimento: str = ""
