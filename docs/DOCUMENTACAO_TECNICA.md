# Documentação Técnica — LIZA

## 1. Arquitetura em Camadas

```text
main.py
└── src/
    ├── config/settings.py       # Variáveis de ambiente (.env) e resource_path()
    ├── domain/usuario.py        # Entidade Usuario (@dataclass)
    ├── services/
    │   ├── auth_service.py      # Autenticação/Cadastro (SQLite padrão / MySQL opcional) + bcrypt
    │   ├── session_service.py   # Persistência local opcional de sessão ("Manter conectado")
    │   └── weather_service.py   # Cliente OpenWeatherMap (HTTPS + timeout)
    ├── core/
    │   ├── speech.py            # SpeechEngine (STT + TTS thread-safe com Lock)
    │   ├── command_router.py    # Carregamento e matching de data/commands.json
    │   └── actions.py           # ActionExecutor desacoplado da UI e do TTS
    └── ui/
        ├── app.py               # Janela CTk (1200x620) e atalho global F1
        ├── login_frame.py       # Tela de autenticação e cadastro local
        └── home_frame.py        # Tela principal com execução assíncrona em thread
```

## 2. Decisões de Arquitetura e Segurança

- **Desacoplamento de Thread na UI:** A captura de voz (`SpeechEngine.listen`) e a síntese (`SpeechEngine.speak`) rodam em `threading.Thread(daemon=True)`, atualizando a interface via `self.after(0, ...)` para evitar congelamento do Tkinter.
- **Banco de Dados Híbrido:** O projeto utiliza **SQLite local** por padrão (`DB_BACKEND=sqlite`), com criação automática da tabela `Usuario` em `data/liza.db`. Caso um servidor MySQL esteja configurado, basta definir `DB_BACKEND=mysql` e as credenciais no `.env`.
- **Proteção de Credenciais:** Nenhuma senha ou chave de API é armazenada no código-fonte. Senhas de usuários são armazenadas como hash `bcrypt`.
- **Extensibilidade de Comandos:** Novos comandos podem ser adicionados em `data/commands.json` usando curinga `*` no padrão e `{query}` no template de URL.

## 3. Testes, Cobertura e Self-Test

- **Testes unitários e cobertura (`> 70%`):**
  ```powershell
  pytest --cov=src --cov-report=term-missing -v
  ```
- **Self-Test automatizado (logs e tempos):**
  ```powershell
  python -m scripts.self_test
  ```
  Gera o relatório em `logs/self_test_report.log`.
