from src.core.command_router import CommandRouter


def test_match_fixed_command():
    router = CommandRouter()
    match = router.match("qual o clima hoje")
    assert match is not None
    assert match.action == "temp"
    assert match.argument == ""


def test_match_wildcard_command():
    router = CommandRouter()
    match = router.match("pesquise por Python assíncrono")
    assert match is not None
    assert match.action.startswith("web?:")
    assert match.argument == "python assíncrono"


def test_match_unknown_command_returns_none():
    router = CommandRouter()
    assert router.match("comando inexistente xyz") is None


def test_commands_json_has_no_duplicate_patterns():
    router = CommandRouter()
    seen: set[str] = set()
    duplicates: list[str] = []
    for section_group in router.voice_commands:
        for commands in section_group.values():
            for entry in commands:
                pattern = next(iter(entry.keys())).strip().lower()
                if pattern in seen:
                    duplicates.append(pattern)
                seen.add(pattern)
    assert duplicates == []


def test_add_and_remove_user_command(tmp_path):
    user_file = tmp_path / "user_commands.json"
    router = CommandRouter(user_commands_file=user_file)

    router.add_user_command("abrir github", "web!:https://github.com")
    match = router.match("abrir github")
    assert match is not None
    assert match.action == "web!:https://github.com"

    assert router.remove_user_command("abrir github") is True
    assert router.match("abrir github") is None
