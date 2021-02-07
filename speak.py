import pyttsx3

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('language','hi')


def speak(audio):
    engine.say(audio)
    
    engine.runAndWait()


speak("bhos dk")    