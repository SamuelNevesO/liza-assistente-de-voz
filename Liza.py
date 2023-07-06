import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import json
from modules import controle

class AI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.SOM_INICIO = AudioSegment.from_wav("bip.wav")
        self.tts_engine = pyttsx3.init()
        self.VOICE_COMMANDS = []
        self.read_commands_file()


    def speak(self, text):
        if self.tts_engine._inLoop:
            self.tts_engine.endLoop()
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        play(self.SOM_INICIO)

        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, None, 5)
            voice_data = ""
            try:
                voice_data = self.recognizer.recognize_google(
                    audio, language="pt-BR"
                ).lower()
            except sr.UnknownValueError:
                self.speak("Desculpe, não entendi")
            except sr.RequestError:
                self.speak("Desculpe, o serviço está offline")

            print("Liza>> ", voice_data.lower())
            if voice_data:
                success = self.check_commands(voice_data)
                if not success:
                    self.speak("Não consegui entender o comando")

    def read_commands_file(self):
        with open("commands.json", "rb") as commands_file:
            commands = json.load(commands_file)
            self.VOICE_COMMANDS = commands['commands']
    
            
    def check_command_matching(self, term, command):
        if term.strip() == command.strip():
            return True
        return False


    def extract_argument(self, command_text, voice_command):
        splitted_text = command_text.split(voice_command.replace("*", ""), 1)

        argument = ""
        if len(splitted_text) > 1:
            argument = splitted_text[1]
        else:
            argument = splitted_text[0]

        return argument
        
    def check_commands(self, command_text):
        for command_section_list in self.VOICE_COMMANDS:
            for command_section, commands in command_section_list.items():
                for command in commands:
                    voice_command = next(iter(command))
                    command_action = command[voice_command]
                    argument = ""

                    if "*" in voice_command:
                        argument = self.extract_argument(command_text, voice_command)

                    voice_command = voice_command.replace("*", argument)
                    found_action = self.check_command_matching(
                        voice_command, command_text
                    )

                    if found_action:
                        try:
                            return self.run_commands(command_section, command_action, argument)
                        except:
                            self.speak(f"Ocorreu um problema no comando {voice_command}. Tente de novo")
                            return False
        return False

    def run_commands(self, command_type, command_action, argument):
        if command_type == "abrir":
            controle.parse_command(self, command_action, argument)
            return True
        return False
