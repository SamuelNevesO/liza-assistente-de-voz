from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from typing import Iterator

import bcrypt

from src.config.settings import Settings
from src.domain.usuario import Usuario

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Erro operacional na camada de autenticação."""


class AuthService:
    """Gerencia cadastro e autenticação de usuários em SQLite (padrão) ou MySQL."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if self.settings.db_backend == "sqlite":
            self._init_sqlite()

    def _init_sqlite(self) -> None:
        with self._sqlite_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Usuario (
                    email TEXT PRIMARY KEY,
                    senha TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    data_nascimento TEXT DEFAULT ''
                )
                """
            )
            conn.commit()

    @contextmanager
    def _sqlite_connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.settings.sqlite_path)
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def _mysql_connection(self):
        try:
            import mysql.connector
        except ImportError as exc:
            raise AuthError("Dependência mysql-connector-python não instalada.") from exc

        try:
            conn = mysql.connector.connect(
                host=self.settings.db_host,
                user=self.settings.db_user,
                password=self.settings.db_password,
                database=self.settings.db_name,
                connection_timeout=5,
            )
        except Exception as exc:
            logger.exception("Falha ao conectar no MySQL")
            raise AuthError("Não foi possível conectar ao servidor MySQL.") from exc

        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def hash_password(senha: str) -> str:
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(senha: str, stored_hash: str) -> bool:
        try:
            return bcrypt.checkpw(senha.encode("utf-8"), stored_hash.encode("utf-8"))
        except ValueError:
            return False

    def registrar(
        self,
        email: str,
        senha: str,
        nome: str,
        data_nascimento: str = "",
    ) -> Usuario:
        email_norm = email.strip().lower()
        nome_norm = nome.strip()
        if not email_norm or not senha or not nome_norm:
            raise AuthError("Preencha e-mail, nome e senha.")

        senha_hash = self.hash_password(senha)

        if self.settings.db_backend == "mysql":
            return self._registrar_mysql(email_norm, senha_hash, nome_norm, data_nascimento.strip())
        return self._registrar_sqlite(email_norm, senha_hash, nome_norm, data_nascimento.strip())

    def _registrar_sqlite(
        self, email: str, senha_hash: str, nome: str, data_nascimento: str
    ) -> Usuario:
        try:
            with self._sqlite_connection() as conn:
                conn.execute(
                    "INSERT INTO Usuario (email, senha, nome, data_nascimento) VALUES (?, ?, ?, ?)",
                    (email, senha_hash, nome, data_nascimento),
                )
                conn.commit()
        except sqlite3.IntegrityError as exc:
            raise AuthError("Já existe um usuário cadastrado com esse e-mail.") from exc
        return Usuario(email=email, nome=nome, data_nascimento=data_nascimento)

    def _registrar_mysql(
        self, email: str, senha_hash: str, nome: str, data_nascimento: str
    ) -> Usuario:
        with self._mysql_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Usuario (email, senha, nome, data_nascimento) VALUES (%s, %s, %s, %s)",
                    (email, senha_hash, nome, data_nascimento),
                )
                conn.commit()
            except Exception as exc:
                raise AuthError("Não foi possível cadastrar o usuário no MySQL.") from exc
            finally:
                cursor.close()
        return Usuario(email=email, nome=nome, data_nascimento=data_nascimento)

    def autenticar(self, email: str, senha: str) -> Usuario | None:
        email_norm = email.strip().lower()
        if not email_norm or not senha:
            return None

        if self.settings.db_backend == "mysql":
            row = self._buscar_mysql(email_norm)
        else:
            row = self._buscar_sqlite(email_norm)

        if not row:
            return None

        stored_email, stored_hash, nome, data_nascimento = row
        if not self.verify_password(senha, stored_hash):
            return None

        return Usuario(
            email=stored_email,
            nome=nome or stored_email,
            data_nascimento=data_nascimento or "",
        )

    def _buscar_sqlite(self, email: str):
        with self._sqlite_connection() as conn:
            cursor = conn.execute(
                "SELECT email, senha, nome, data_nascimento FROM Usuario WHERE email = ?",
                (email,),
            )
            return cursor.fetchone()

    def _buscar_mysql(self, email: str):
        with self._mysql_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "SELECT email, senha, nome, data_nascimento FROM Usuario WHERE email = %s",
                    (email,),
                )
                return cursor.fetchone()
            finally:
                cursor.close()
