from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import pywhatkit as kit
import youtube_search
from youtubesearchpython import SearchVideos
from playsound import playsound
import random
import smtplib
import wikipedia
import pywhatkit
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
conn = sqlite3.connect("contacts.db")
c = conn.cursor()

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()

get_audio()    
