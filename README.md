# LIZA — Assistente de Voz para Acessibilidade Digital

Aplicação desktop em Python desenvolvida como projeto de extensão (UCSAL) para auxiliar pessoas com limitações motoras, idosos e usuários em geral a interagirem com o computador e serviços web por meio de comandos de voz em português brasileiro.

## Principais Recursos

- **Reconhecimento e síntese de voz (PT-BR):** captura de áudio via `SpeechRecognition` e retorno falado via `pyttsx3` em thread separada (sem travar a interface).
- **Atalho global `F1`:** permite acionar a escuta mesmo quando outra janela (como o navegador) está em foco.
- **Comandos configuráveis em JSON:** buscas no Google, YouTube, Wikipedia, Spotify, tradução, notícias, previsão do tempo (`OpenWeatherMap`), além de atalhos locais (`ajuda`, `abrir calculadora`, `abrir bloco de notas`).
- **Autenticação segura e acessibilidade:** login/cadastro local com `SQLite` + `bcrypt` (com suporte opcional a `MySQL`) e opção **"Manter conectado"**.

## Início Rápido

```powershell
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Documentação

- [Guia de Instalação](docs/GUIA_INSTALACAO.md)
- [Manual do Usuário](docs/MANUAL_USUARIO.md)
- [Documentação Técnica](docs/DOCUMENTACAO_TECNICA.md)

## Testes e Self-Test

```powershell
pytest --cov=src --cov-report=term-missing -v
python -m scripts.self_test
```
