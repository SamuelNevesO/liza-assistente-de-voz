from __future__ import annotations

import logging
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from src.config.settings import Settings, app_data_path, resource_path
from src.core.actions import ActionExecutor
from src.core.command_router import CommandRouter
from src.services.auth_service import AuthService
from src.services.weather_service import WeatherService


@dataclass
class CheckResult:
    name: str
    passed: bool
    duration_ms: float
    detail: str


def run_self_test() -> list[CheckResult]:
    results: list[CheckResult] = []

    def execute_check(name: str, fn) -> None:
        start = time.perf_counter()
        try:
            detail = fn()
            elapsed = (time.perf_counter() - start) * 1000
            results.append(CheckResult(name=name, passed=True, duration_ms=elapsed, detail=detail))
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            results.append(CheckResult(name=name, passed=False, duration_ms=elapsed, detail=str(exc)))

    def check_assets() -> str:
        required = [resource_path("assets/liza.png"), resource_path("assets/bip.wav")]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise FileNotFoundError(f"Assets ausentes: {', '.join(missing)}")
        return "liza.png e bip.wav encontrados."

    def check_commands_integrity() -> str:
        router = CommandRouter()
        total = sum(len(cmds) for group in router.voice_commands for cmds in group.values())
        if total == 0:
            raise ValueError("Nenhum comando carregado em data/commands.json")
        return f"{total} comandos carregados e validados."

    def check_command_execution() -> str:
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(
                db_backend="sqlite",
                sqlite_path=Path(tmp) / "selftest.db",
                db_host="localhost",
                db_user="root",
                db_password="",
                db_name="liza",
                openweather_api_key="",
                weather_city="Salvador,BR",
            )
            router = CommandRouter()
            executor = ActionExecutor(router, WeatherService(settings))
            with patch("src.core.actions.webbrowser.open_new") as mock_browser:
                for phrase in ("ajuda", "pesquise por acessibilidade", "qual o clima hoje"):
                    match = router.match(phrase)
                    if match is None:
                        raise AssertionError(f"Falha no matching de '{phrase}'")
                    executor.execute(match)
                if mock_browser.call_count != 1:
                    raise AssertionError("Esperava 1 abertura de navegador mockada.")
        return "Roteamento e execução validados."

    def check_auth_sqlite() -> str:
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(
                db_backend="sqlite",
                sqlite_path=Path(tmp) / "auth_selftest.db",
                db_host="localhost",
                db_user="root",
                db_password="",
                db_name="liza",
                openweather_api_key="",
                weather_city="Salvador,BR",
            )
            auth = AuthService(settings)
            auth.registrar("selftest@liza.app", "senha123", "Self Test")
            user = auth.autenticar("selftest@liza.app", "senha123")
            if user is None:
                raise AssertionError("Falha ao autenticar usuário recém-cadastrado.")
        return "Cadastro e autenticação SQLite com bcrypt validados."

    execute_check("Assets obrigatórios", check_assets)
    execute_check("Integridade de commands.json", check_commands_integrity)
    execute_check("Roteamento e execução de comandos", check_command_execution)
    execute_check("Autenticação local (SQLite + bcrypt)", check_auth_sqlite)
    return results


def write_report(results: list[CheckResult]) -> Path:
    report_path = app_data_path("logs/self_test_report.log")
    total_ms = sum(r.duration_ms for r in results)
    passed_count = sum(1 for r in results if r.passed)

    lines = [
        f"LIZA Self-Test Report - {datetime.now().isoformat(timespec='seconds')}",
        "=" * 64,
    ]
    for item in results:
        status = "PASS" if item.passed else "FAIL"
        lines.append(f"[{status}] {item.name} ({item.duration_ms:.2f} ms) - {item.detail}")
    lines.append("=" * 64)
    lines.append(f"Resumo: {passed_count}/{len(results)} aprovados | Tempo total: {total_ms:.2f} ms")

    content = "\n".join(lines) + "\n"
    report_path.write_text(content, encoding="utf-8")
    return report_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    check_results = run_self_test()
    path = write_report(check_results)
    print(path.read_text(encoding="utf-8"))
    if any(not r.passed for r in check_results):
        raise SystemExit(1)
