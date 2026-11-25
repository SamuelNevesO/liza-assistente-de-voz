from __future__ import annotations

import logging
import requests

from src.config.settings import Settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Consulta temperatura atual via OpenWeatherMap."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, settings: Settings) -> None:
        self.api_key = settings.openweather_api_key
        self.default_city = settings.weather_city or "Salvador,BR"

    def get_temperature(self, city: str | None = None) -> int | None:
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY não configurada.")
            return None

        target_city = (city or self.default_city).strip()
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "q": target_city,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "pt_br",
                },
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            return int(round(data["main"]["temp"]))
        except (requests.RequestException, KeyError, TypeError, ValueError):
            logger.exception("Erro ao consultar temperatura para %s", target_city)
            return None
