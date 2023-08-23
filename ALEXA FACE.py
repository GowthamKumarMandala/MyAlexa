import face_recognition
import cv2
import os
import glob
import numpy as np

owner :bool = False
name = ""

#ALEXA CODE

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
engine.setProperty('rate',170)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("I'm Listening...")
            talk("I'm Listening...")
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
    if 'play' in command or 'youtube' in command :
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
            print(b)
            talk("your name is "+b[3])
              
    elif 'whatsapp' in command:
        talk("opening whatsapp")
        wb.open("https://web.whatsapp.com")
    elif 'open' in command:
        command = command.replace('open','')
        talk("opening"+command)
        print("opening",command)
        #wb.open("https://www.google.com/search?q="+command+"&rlz=1C1ONGR_enIN1001IN1001&oq=&aqs=chrome.0.35i39i362l8.2418055963j0j15&sourceid=chrome&ie=UTF-8")
        wb.open("https://www.google.com/")
    elif 'images' in command:
        command = command.replace('image','')
        wb.open("https://www.bing.com/images/search?q="+command+"&form=HDRSC2&first=1&tsc=ImageHoverTitle")



#COMMAND FOR DETECTING NAMES AND GETTING NAMES FROM IMAGES FOLDER
class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            if img is None:
                print("Failed to load image:", img_path)
                talk("Failed to load image:"+ img_path)
                continue

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            
            img_encoding = face_recognition.face_encodings(rgb_img)
            if len(img_encoding) > 0:
                self.known_face_encodings.append(img_encoding[0])
                self.known_face_names.append(filename)
            else:
                talk("No face found in image:"+ img_path)

        print("Encoding images loaded")
        

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations) / self.frame_resizing
        return face_locations.astype(int), face_names

sfr = SimpleFacerec()

sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(0) 
print("face recognition started..")
talk("face recognition started..")
print("Enter 'Escape' key to stop recoginition process..")
talk("Enter 'Escape' key to stop recoginition process..")
while True:
    ret, frame = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break          
cap.release()
cv2.destroyAllWindows()
if(name=="gow2"):
    owner = True
else:
    owner = False
if(owner):
    talk("FACE Detected as my BOSS GOWTHAM KUMAR")
    talk("tell me GOWTHAM BOSS ")
    talk("what can i do for you")
    while(7):
        run_alexa()
else:
    talk("face detected as unknown")
    talk("what is your name")
    run_alexa()
    talk("HELLO! "+name)
    talk("what can i do for you")
    while(7):
         run_alexa()
    

