from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

from src.config.settings import Settings, app_data_path

logger = logging.getLogger(__name__)


@dataclass
class UserConfig:
    """Preferências editáveis pelo usuário na interface."""

    openweather_api_key: str = ""
    weather_city: str = "Salvador,BR"
    tts_rate: int = 180


class UserConfigService:
    """Lê e persiste configurações editáveis do usuário em JSON gravável."""

    def __init__(self, settings: Settings, config_file: Path | None = None) -> None:
        self.settings = settings
        self.config_file = config_file or app_data_path("data/user_config.json")

    def load(self) -> UserConfig:
        base = UserConfig(
            openweather_api_key=self.settings.openweather_api_key,
            weather_city=self.settings.weather_city or "Salvador,BR",
            tts_rate=180,
        )
        if not self.config_file.exists():
            return base

        try:
            raw = json.loads(self.config_file.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Falha ao ler user_config.json; usando valores padrão.")
            return base

        api_key = str(raw.get("openweather_api_key", "")).strip() or base.openweather_api_key
        city = str(raw.get("weather_city", "")).strip() or base.weather_city
        try:
            rate = int(raw.get("tts_rate", base.tts_rate))
        except (TypeError, ValueError):
            rate = base.tts_rate

        return UserConfig(
            openweather_api_key=api_key,
            weather_city=city,
            tts_rate=max(100, min(300, rate)),
        )

    def save(self, config: UserConfig) -> UserConfig:
        normalized = UserConfig(
            openweather_api_key=config.openweather_api_key.strip(),
            weather_city=config.weather_city.strip() or "Salvador,BR",
            tts_rate=max(100, min(300, int(config.tts_rate))),
        )
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(
            json.dumps(asdict(normalized), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return normalized
