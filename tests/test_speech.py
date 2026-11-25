from unittest.mock import MagicMock

import speech_recognition as sr

from src.core.speech import SpeechEngine


def _make_engine(monkeypatch):
    mock_tts = MagicMock()
    monkeypatch.setattr("src.core.speech.pyttsx3.init", MagicMock(return_value=mock_tts))
    engine = SpeechEngine()
    monkeypatch.setattr(engine.recognizer, "adjust_for_ambient_noise", MagicMock())
    return engine, mock_tts


def test_speak_calls_tts_engine(monkeypatch):
    engine, mock_tts = _make_engine(monkeypatch)
    engine.speak("Olá mundo")
    mock_tts.say.assert_called_once_with("Olá mundo")
    mock_tts.runAndWait.assert_called_once()


def test_listen_returns_recognized_text(monkeypatch):
    engine, _ = _make_engine(monkeypatch)
    mock_mic = MagicMock()
    mock_mic.__enter__.return_value = MagicMock()
    monkeypatch.setattr("src.core.speech.sr.Microphone", MagicMock(return_value=mock_mic))
    monkeypatch.setattr(engine.recognizer, "listen", MagicMock(return_value=b"audio"))
    monkeypatch.setattr(engine.recognizer, "recognize_google", MagicMock(return_value="Qual o clima hoje"))

    result = engine.listen()
    assert result.text == "qual o clima hoje"
    assert result.error_message == ""


def test_listen_handles_unknown_value(monkeypatch):
    engine, _ = _make_engine(monkeypatch)
    mock_mic = MagicMock()
    mock_mic.__enter__.return_value = MagicMock()
    monkeypatch.setattr("src.core.speech.sr.Microphone", MagicMock(return_value=mock_mic))
    monkeypatch.setattr(engine.recognizer, "listen", MagicMock(return_value=b"audio"))
    monkeypatch.setattr(
        engine.recognizer, "recognize_google", MagicMock(side_effect=sr.UnknownValueError())
    )

    result = engine.listen()
    assert result.text == ""
    assert "não entendi" in result.error_message.lower()
