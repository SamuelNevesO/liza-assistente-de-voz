from __future__ import annotations

import logging
import subprocess
import webbrowser
from urllib.parse import quote_plus

from src.core.command_router import CommandMatch, CommandRouter
from src.services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Executa ações desacopladas da UI e da síntese de voz, retornando mensagem de feedback."""

    def __init__(self, router: CommandRouter, weather_service: WeatherService) -> None:
        self.router = router
        self.weather_service = weather_service

    def execute(self, match: CommandMatch) -> str:
        action = match.action.strip()
        argument = match.argument.strip()

        if action == "help":
            return (
                "Você pode pedir para pesquisar no Google, YouTube, Wikipedia ou Spotify, "
                "consultar o clima de hoje, ou abrir a calculadora e o bloco de notas."
            )

        if action.startswith("web!:"):
            self.open_link(action[5:])
            return "Abrindo página."

        if action.startswith("web?:"):
            url = self.build_search_url(action[5:], argument)
            self.open_link(url)
            return f"Pesquisando {argument}"

        if action.startswith("spo!:"):
            url = self.build_search_url(action[5:], argument, default_suffix="/search/{query}")
            self.open_link(url)
            return f"Abrindo Spotify para {argument}"

        if action.startswith("path:"):
            target = action[5:]
            self.open_program(target)
            label = argument or target.replace(".exe", "")
            return f"Abrindo {label}"

        if action == "commands":
            self.router.reload()
            return "Comandos atualizados."

        if action == "temp" or action.startswith("weather:"):
            city = action[8:].strip() if action.startswith("weather:") else None
            temp_now = self.weather_service.get_temperature(city=city)
            if temp_now is None:
                return "Não foi possível obter a temperatura no momento."
            city_label = city or self.weather_service.default_city
            return f"A temperatura atual em {city_label} é de {temp_now} graus Celsius."

        logger.warning("Ação desconhecida: %s", action)
        return "Comando reconhecido, mas sem ação configurada."

    @staticmethod
    def build_search_url(
        template: str, argument: str, default_suffix: str = "/search?q={query}"
    ) -> str:
        encoded = quote_plus(argument)
        if "{query}" in template:
            return template.replace("{query}", encoded)
        return f"{template.rstrip('/')}{default_suffix.replace('{query}', encoded)}"

    @staticmethod
    def open_link(url: str) -> None:
        webbrowser.open_new(url)

    @staticmethod
    def open_program(path: str) -> None:
        subprocess.Popen([path])
