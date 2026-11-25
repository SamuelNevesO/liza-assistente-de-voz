from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from src.config.settings import app_data_path, resource_path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CommandMatch:
    """Representa um comando reconhecido e seu argumento extraído."""

    section: str
    action: str
    argument: str = ""
    pattern: str = ""


class CommandRouter:
    """Carrega comandos base e comandos customizados do usuário e realiza o matching."""

    def __init__(
        self,
        commands_file: Path | None = None,
        user_commands_file: Path | None = None,
    ) -> None:
        self.commands_file = commands_file or resource_path("data/commands.json")
        self.user_commands_file = user_commands_file or app_data_path("data/user_commands.json")
        self.voice_commands: list[dict] = []
        self.reload()

    def reload(self) -> None:
        with open(self.commands_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        base_commands = data.get("commands", [])

        user_entries = self.list_user_commands()
        if user_entries:
            self.voice_commands = [{"abrir": user_entries}, *base_commands]
        else:
            self.voice_commands = base_commands

    def list_user_commands(self) -> list[dict[str, str]]:
        if not self.user_commands_file.exists():
            return []
        try:
            data = json.loads(self.user_commands_file.read_text(encoding="utf-8"))
            items = data.get("commands", [])
            return [item for item in items if isinstance(item, dict) and len(item) == 1]
        except Exception:
            logger.warning("Falha ao ler user_commands.json; ignorando.")
            return []

    def add_user_command(self, phrase: str, action: str) -> None:
        normalized_phrase = " ".join(phrase.strip().lower().split())
        clean_action = action.strip()
        if not normalized_phrase or not clean_action:
            raise ValueError("Informe a frase de voz e a ação do comando.")

        current = self.list_user_commands()
        filtered = [
            entry for entry in current if next(iter(entry.keys())).strip().lower() != normalized_phrase
        ]
        filtered.append({normalized_phrase: clean_action})
        self._save_user_commands(filtered)
        self.reload()

    def remove_user_command(self, phrase: str) -> bool:
        normalized_phrase = " ".join(phrase.strip().lower().split())
        current = self.list_user_commands()
        filtered = [
            entry for entry in current if next(iter(entry.keys())).strip().lower() != normalized_phrase
        ]
        if len(filtered) == len(current):
            return False
        self._save_user_commands(filtered)
        self.reload()
        return True

    def _save_user_commands(self, entries: list[dict[str, str]]) -> None:
        self.user_commands_file.parent.mkdir(parents=True, exist_ok=True)
        self.user_commands_file.write_text(
            json.dumps({"commands": entries}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def extract_argument(command_text: str, pattern: str) -> str:
        prefix = pattern.split("*", 1)[0].strip()
        text = command_text.strip()
        if not prefix:
            return text
        if text.startswith(prefix):
            return text[len(prefix) :].strip()
        parts = text.split(prefix, 1)
        return parts[1].strip() if len(parts) > 1 else parts[0].strip()

    def match(self, command_text: str) -> CommandMatch | None:
        normalized = " ".join(command_text.strip().lower().split())
        if not normalized:
            return None

        for section_group in self.voice_commands:
            for section, commands in section_group.items():
                for entry in commands:
                    pattern, action = next(iter(entry.items()))
                    pattern_norm = " ".join(pattern.strip().lower().split())

                    if "*" in pattern_norm:
                        prefix, suffix = pattern_norm.split("*", 1)
                        prefix = prefix.strip()
                        suffix = suffix.strip()
                        if normalized.startswith(prefix) and normalized.endswith(suffix):
                            end_idx = len(normalized) - len(suffix) if suffix else len(normalized)
                            argument = normalized[len(prefix) : end_idx].strip()
                            if argument:
                                return CommandMatch(
                                    section=section,
                                    action=action,
                                    argument=argument,
                                    pattern=pattern,
                                )
                    elif normalized == pattern_norm:
                        return CommandMatch(
                            section=section,
                            action=action,
                            argument="",
                            pattern=pattern,
                        )
        return None
