from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.config.settings import resource_path


@dataclass(frozen=True)
class CommandMatch:
    """Representa um comando reconhecido e seu argumento extraído."""

    section: str
    action: str
    argument: str = ""
    pattern: str = ""


class CommandRouter:
    """Carrega comandos de um arquivo JSON e realiza o matching por texto."""

    def __init__(self, commands_file: Path | None = None) -> None:
        self.commands_file = commands_file or resource_path("data/commands.json")
        self.voice_commands: list[dict] = []
        self.reload()

    def reload(self) -> None:
        with open(self.commands_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.voice_commands = data.get("commands", [])

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
