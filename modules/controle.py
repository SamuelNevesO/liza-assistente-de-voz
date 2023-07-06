import webbrowser
import subprocess

def parse_command(liza, command_action, argument=""):
    if command_action[0:4] == "web!":
        open_link(command_action[5:])
    elif command_action[0:4] == "web?":
        open_link_with_search(command_action[5:], argument)
        liza.speak("Pesquisando " + argument)
    elif command_action[0:4] == "path":
        open_program(command_action[5:])
        liza.speak("Abrindo " + argument)
    elif command_action == 'commands':
        liza.read_commands_file()
        liza.speak("Atualizado")

def open_link_with_search(link, argument=""):
    print(f'{link}/search?q={argument}')
    webbrowser.get('windows-default').open_new(f'{link}/search?q={argument}')

def open_link(link):
    webbrowser.get('windows-default').open_new(f'{link}')

def open_program(path):
    subprocess.Popen([path, '-new-tab'])