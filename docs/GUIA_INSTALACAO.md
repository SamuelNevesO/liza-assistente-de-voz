# Guia de Instalação — LIZA

## 1. Pré-requisitos

- **Sistema Operacional:** Windows 10 ou 11 (recomendado para `pyttsx3` SAPI5 e atalho global `F1`).
- **Python:** 3.11 ou superior.
- **Microfone funcional** conectado ao computador (necessário apenas para captura de voz).

## 2. Instalação das Dependências

No diretório raiz do projeto, execute:

```powershell
python -m pip install -r requirements.txt
```

> **Nota sobre PyAudio (microfone):** Caso o `SpeechRecognition` solicite `PyAudio` no Windows, instale com `pip install pyaudio`.

## 3. Configuração de Variáveis de Ambiente (`.env`)

1. Copie o arquivo de exemplo:
   ```powershell
   copy .env.example .env
   ```
2. Edite o `.env` caso queira configurar:
   - `OPENWEATHER_API_KEY`: chave gratuita da OpenWeatherMap para o comando `"qual o clima hoje"`.
   - `WEATHER_CITY`: cidade padrão (ex.: `Salvador,BR`).
   - `DB_BACKEND`: `sqlite` (padrão local) ou `mysql` (opcional).

## 4. Executando a Aplicação

```powershell
python main.py
```

## 5. Gerando Executável (`.exe`) com PyInstaller

```powershell
pyinstaller liza.spec
```

O executável será gerado em `dist/Liza.exe` já com `assets/` e `data/commands.json` empacotados.
