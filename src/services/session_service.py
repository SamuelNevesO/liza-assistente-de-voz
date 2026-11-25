from __future__ import annotations

import json
import logging
from pathlib import Path

from src.config.settings import app_data_path
from src.domain.usuario import Usuario

logger = logging.getLogger(__name__)


class SessionService:
    """Persiste opcionalmente a sessão do usuário para acessibilidade ("Manter conectado")."""

    def __init__(self, session_file: Path | None = None) -> None:
        self.session_file = session_file or app_data_path("data/session.json")

    def save(self, usuario: Usuario) -> None:
        payload = {
            "email": usuario.email,
            "nome": usuario.nome,
            "data_nascimento": usuario.data_nascimento,
        }
        self.session_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def load(self) -> Usuario | None:
        if not self.session_file.exists():
            return None
        try:
            data = json.loads(self.session_file.read_text(encoding="utf-8"))
            email = str(data.get("email", "")).strip()
            nome = str(data.get("nome", "")).strip()
            if not email or not nome:
                return None
            return Usuario(
                email=email,
                nome=nome,
                data_nascimento=str(data.get("data_nascimento", "")),
            )
        except Exception:
            logger.warning("Falha ao carregar sessão salva; ignorando.")
            return None

    def clear(self) -> None:
        if self.session_file.exists():
            self.session_file.unlink()
