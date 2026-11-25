from __future__ import annotations

import logging
import time
import requests

from src.config.settings import Settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Consulta temperatura atual via OpenWeatherMap com cache TTL em memória."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    CACHE_TTL_SECONDS = 600

    def __init__(self, settings: Settings) -> None:
        self.api_key = settings.openweather_api_key
        self.default_city = settings.weather_city or "Salvador,BR"
        self._cache: dict[str, tuple[float, int]] = {}

    def configure(self, api_key: str, city: str) -> None:
        self.api_key = api_key.strip()
        self.default_city = city.strip() or "Salvador,BR"
        self._cache.clear()

    def get_temperature(self, city: str | None = None) -> int | None:
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY não configurada.")
            return None

        target_city = (city or self.default_city).strip()
        cache_key = target_city.lower()
        now = time.monotonic()
        cached = self._cache.get(cache_key)
        if cached is not None and (now - cached[0]) < self.CACHE_TTL_SECONDS:
            return cached[1]

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
            temp = int(round(data["main"]["temp"]))
            self._cache[cache_key] = (now, temp)
            return temp
        except (requests.RequestException, KeyError, TypeError, ValueError):
            logger.exception("Erro ao consultar temperatura para %s", target_city)
            return None

    def test_connection(self, api_key: str, city: str) -> tuple[bool, str]:
        key = api_key.strip()
        target_city = city.strip() or self.default_city
        if not key:
            return False, "Informe uma API Key antes de testar."
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "q": target_city,
                    "appid": key,
                    "units": "metric",
                    "lang": "pt_br",
                },
                timeout=5,
            )
            if response.status_code == 401:
                return False, "API Key inválida ou ainda não ativada."
            response.raise_for_status()
            data = response.json()
            temp = int(round(data["main"]["temp"]))
            return True, f"Conexão OK! {target_city}: {temp} °C."
        except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
            return False, f"Falha ao conectar: {exc}"
