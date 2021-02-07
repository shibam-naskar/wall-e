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



x = datetime.datetime.now()

date = x.day
month = x.month


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]



def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('hellowiamwalle@gmail.com', 'Shibam@2000')
    server.sendmail('hellowiamwalle@gmail.com', to, content)
    server.close()
    

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


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    # THE NEW PART STARTS HERE
    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


WAKE = "wali"
SERVICE = authenticate_google()
print("Start")

while True:
    print("Listening")
    text = get_audio()

    if text.count(WAKE) > 0:
        sounds = ['voice.1.mp3','WALLE 4.mp3','Eve 2.mp3','Whoa.mp3']
        final_sound = random.choice(sounds)
        playsound(final_sound)
        text = get_audio()

        CALENDAR_STRS = ["what do I have", "do I have plan", "am i busy", "my plan"]
        for phrase in CALENDAR_STRS:
            if phrase in text:
                date = get_date(text)
                if date:
                    get_events(date, SERVICE)
                else:
                    speak("I don't understand")

        NOTE_STRS = ["make a note", "write this down", "remember this","take a note","note it","note it down","noted down"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down?")
                note_text = get_audio()
                note(note_text)
                speak("I've made a note of that.")

        NOTE_STRS = ["play"]
        for phrase in NOTE_STRS:
            if phrase in text:
                text = text.replace(phrase, "")
                speak("ok playing it")
                kit.playonyt(text) 

        NOTE_STRS = ["can you make"]
        for phrase in NOTE_STRS:
            if phrase in text:
                text = text.replace(phrase, "")
                playsound("make.mp3")

        NOTE_STRS = ["wikipedia"]
        for phrase in NOTE_STRS:
            if phrase in text:
                text = text.replace(phrase, "")
                count = len(text.split())
                try:
                    if count>0:

                         results = wikipedia.summary(text, sentences=2)
                         speak("According to Wikipedia")
                         print(results)
                         speak(results)
                    else:
                         speak("wikipedia is on .what do i search?")
                         print("listning..")
                         what = get_audio()
                         results = wikipedia.summary(what, sentences=2)
                         speak("According to Wikipedia")
                         print(results)
                         speak(results)
                except :
                    speak("can't find any thing acording to you")


        NOTE_STRS = ["today is my birthday","this is my birthday","wish me this is my birthday","it's my birthday","today's my birthday"]
        for phrase in NOTE_STRS:
            if phrase in text:
                
                playsound("birthday.mp3")  


        NOTE_STRS = ["today date","date today","what's the date","what is the date","what is the date today"]
        for phrase in NOTE_STRS:
            if phrase in text:
                
                if ((date==25)&(month==12)):
                    speak("merry christmas")

        NOTE_STRS = ["what's the time","what is the time","the time now","time","time now"]
        for phrase in NOTE_STRS:
            if phrase in text:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")     
                speak(f"Sir, the time is {strTime}")
                break
        NOTE_STRS = ["turn off windows","turn off mechine","shut down windows","shutdown windows","shut down mechine","shut down pc","shutdown pc"]
        for phrase in NOTE_STRS:
            if phrase in text:
                playsound("WALLE 4.mp3")
                pywhatkit.shutdown(time=6)

        NOTE_STRS = ["wish every one","wish","wish everybody","wish all","wish my friend"] 
        for phrase in NOTE_STRS:
            if phrase in text:
                sendEmail('shibamnaskar2@gmail.com','')

               
                
                
                
                
               
                
                
                    

                    
                    
                  
                
                                       

        

                

                
                                       

             