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
