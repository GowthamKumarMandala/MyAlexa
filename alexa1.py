from turtle import speed
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import webbrowser as wb
from tkinter import *
from PIL import Image,ImageTk,ImageSequence

listener = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
engine.setProperty('rate',200)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            
            print("Listening...")
            voice = listener.listen(source,3,5)
            command = listener.recognize_google(voice)
            command=command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','')
                print(command)
    except:
        pass
    return command
def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play','')
        talk('playing'+song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        print(time)
        talk("current time is "+time)
    elif 'what is my name' in command:
        talk('i dont know your name please tell your name')
        
    elif 'my name is' in command:
        if 'gautam' in command:
            print("yes boss i know you,you are my owner and you are my god")
            talk("yes boss i know you,you are my owner and you are my god")
            
        else:
            b=command.split(" ")
            talk("your name is "+b[4])  
    elif 'whatsapp' in command:
        wb.open("https://web.whatsapp.com")
    elif 'open' in command:
        command = command.replace('open','')
        a= command.split(' ')
        #print(a)
        talk("opening"+command)
        print("opening",command)
        wb.open("https://www.bing.com/images/search?q="+command+"&form=HDRSC2&first=1&tsc=ImageHoverTitle")
    elif 'image' in command:
        command = command.replace('image','')
        wb.open("https://www.bing.com/images/search?q="+command+"&form=HDRSC2&first=1&tsc=ImageHoverTitle")
talk("i am your alexa ")
talk("what can i do for you")

while(7):
    run_alexa()
    
