import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import youtube_search
from youtubesearchpython import SearchVideos
import json
import pywhatkit as kit
from playsound import playsound



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am wall e . your assistant . how may i help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en')
        print(f" :- {query}\n")

    except Exception as e:
        # print(e)    
        print("i am sorry i can't recognize it")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('shibamnaskar2@gmail.com', 'shibam123')
    server.sendmail('shibamnaskar2@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'samjhe'in query:
            speak(" yes maam!")   

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("https://www.google.com")

        elif 'open github' in query:
            speak("opening github")
            webbrowser.open("https://github.com")    

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play arijit singh songs' in query:
            speak("here is a song name kaalaank")
            webbrowser.open("https://youtu.be/Grr0FlC8SQA")       


        elif 'play music' in query:
            music_dir = 'C:\\musics'
            songs = os.listdir(music_dir)
            print(songs) 
            speak("here is a song from your collection")   
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")     
            speak(f"Sir, the time is {strTime}")

        elif 'what is your name' in query:
                
            speak("hello my name is wall e") 

        elif 'who are you' in query:
                
            speak("my name is wall e . i am a smirt virtual assistent . i was created by shibam")  

        elif 'wali' in query:
                
            speak("yes sir . how can i help you")

        elif 'will you marry me' in query:
                
            speak("vog bhos          dk ")     
        
        elif 'play' in query:
             query = query.replace("play", "")
             speak("ok playing it")
             kit.playonyt(query)
            
        elif 'open visual studio' in query:
            codePath = "C:\\Users\\shibam\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'open google chrome' in query:
            codePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(codePath)    

        elif 'send mail to shivam' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "shbmnaskar@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("i am having some problems now please try it letter")  

        
                      
