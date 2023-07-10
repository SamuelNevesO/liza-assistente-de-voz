import webbrowser
import subprocess
import requests

def parse_command(liza, command_action, argument=""):
    if command_action[0:4] == "web!":
        open_link(command_action[5:])
    elif command_action[0:4] == "web?":
        open_link_with_search(command_action[5:], argument)
        liza.speak("Pesquisando " + argument)
    elif command_action[0:4] == "path":
        open_program(command_action[5:])
        liza.speak("Abrindo " + argument)
    elif command_action == "commands":
        liza.read_commands_file()
        liza.speak("Atualizado")
    elif command_action[0:4] == "spo!":
        open_link_spotify(command_action[5:], argument)
        liza.speak("Abrindo o site do spotify")
    elif command_action[0:4] == "temp":
        temp_now = temp_get()
        if temp_now is not None:
            liza.speak(f"A temperatura atual em Salvador, Bahia, Brasil é de {temp_now} graus Celsius.")
            print(f"A temperatura atual em Salvador, Bahia, Brasil é de {temp_now} graus Celsius.")
    elif command_action[0:6] == "weather":
        weather_location = command_action[7:]
        current_weather = temp_get_salvador()
        if current_weather is not None:
            liza.speak(f"O clima em {weather_location} é {current_weather}")
            print(f"O clima em {weather_location} é {current_weather}")

def open_link_with_search(link, argument=""):
    print(f"{link}/search?q={argument}")
    webbrowser.get("windows-default").open_new(f"{link}/search?q={argument}")


def open_link_spotify(link, argument=""):
    print(f"{link}/search/{argument}")
    webbrowser.get("windows-default").open_new(f"{link}/search/{argument}")


def open_link(link):
    webbrowser.get("windows-default").open_new(f"{link}")


def open_program(path):
    subprocess.Popen([path, "-new-tab"])


def temp_get_salvador():
    # Insira sua chave de API do OpenWeatherMap aqui
    api_key = "ba3a1a276f95deb0605d29801c65b972"

    # Defina a URL da API com base nas coordenadas de Salvador
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Salvador,BR&appid={api_key}&units=metric"

    # Faz a solicitação GET à API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperatura = int(round(data["main"]["temp"]))
        return temperatura
    else:
        print(
            "Não foi possível obter a temperatura. Verifique sua chave de API e a conexão com a internet."
        )



