from time import sleep
import speech_recognition as sr  # recognise
import keyboard
from Liza import AI

recognizer = sr.Recognizer()

Liza = AI()

while True:
    sleep(0.05)

    if keyboard.is_pressed("'"):
        Liza.listen()
        
    sleep(0.05)
