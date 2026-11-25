from src.domain.usuario import Usuario
from src.services.session_service import SessionService


def test_save_load_and_clear_session(tmp_path):
    session = SessionService(tmp_path / "session.json")
    assert session.load() is None

    user = Usuario(email="ana@liza.app", nome="Ana", data_nascimento="")
    session.save(user)

    loaded = session.load()
    assert loaded == user

    session.clear()
    assert session.load() is None
