from __future__ import annotations

import logging
import threading
from dataclasses import dataclass

import pyttsx3
import speech_recognition as sr

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ListenResult:
    """Resultado de uma captura de voz."""

    text: str = ""
    error_message: str = ""


class SpeechEngine:
    """Encapsula reconhecimento de fala (STT) e síntese de voz (TTS) thread-safe."""

    def __init__(self, language: str = "pt-BR", phrase_time_limit: int = 5) -> None:
        self.language = language
        self.phrase_time_limit = phrase_time_limit
        self.recognizer = sr.Recognizer()
        self._tts_lock = threading.Lock()
        self._tts_engine = pyttsx3.init()

    def speak(self, text: str) -> None:
        if not text:
            return
        with self._tts_lock:
            try:
                self._tts_engine.say(text)
                self._tts_engine.runAndWait()
            except Exception:
                logger.exception("Erro ao reproduzir síntese de voz")

    def listen(self) -> ListenResult:
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(
                    source, timeout=5, phrase_time_limit=self.phrase_time_limit
                )
        except sr.WaitTimeoutError:
            return ListenResult(error_message="Tempo esgotado sem detectar fala.")
        except Exception:
            logger.exception("Erro ao acessar o microfone")
            return ListenResult(error_message="Não foi possível acessar o microfone.")

        try:
            voice_data = self.recognizer.recognize_google(
                audio, language=self.language
            ).lower()
            return ListenResult(text=voice_data.strip())
        except sr.UnknownValueError:
            return ListenResult(error_message="Desculpe, não entendi.")
        except sr.RequestError:
            return ListenResult(error_message="Desculpe, o serviço de voz está offline.")
