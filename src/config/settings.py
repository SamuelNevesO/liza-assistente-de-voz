from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def project_root() -> Path:
    """Retorna a raiz do projeto em desenvolvimento ou o diretório temporário do PyInstaller."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass)
    return Path(__file__).resolve().parents[2]


def resource_path(relative_path: str | Path) -> Path:
    """Resolve caminhos de recursos empacotados (assets, data/commands.json)."""
    return project_root() / relative_path


def app_data_path(relative_path: str | Path) -> Path:
    """Resolve caminhos graváveis em tempo de execução (ex.: banco SQLite local)."""
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parents[2]
    target = base_dir / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


@dataclass(frozen=True)
class Settings:
    """Configurações carregadas a partir de variáveis de ambiente."""

    db_backend: str
    sqlite_path: Path
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    openweather_api_key: str
    weather_city: str

    @classmethod
    def from_env(cls, env_path: Path | None = None) -> "Settings":
        load_dotenv(dotenv_path=env_path or app_data_path(".env"), override=False)
        sqlite_rel = os.getenv("SQLITE_PATH", "data/liza.db")
        return cls(
            db_backend=os.getenv("DB_BACKEND", "sqlite").strip().lower(),
            sqlite_path=app_data_path(sqlite_rel),
            db_host=os.getenv("DB_HOST", "localhost"),
            db_user=os.getenv("DB_USER", "root"),
            db_password=os.getenv("DB_PASSWORD", ""),
            db_name=os.getenv("DB_NAME", "liza"),
            openweather_api_key=os.getenv("OPENWEATHER_API_KEY", "").strip(),
            weather_city=os.getenv("WEATHER_CITY", "Salvador,BR").strip(),
        )
