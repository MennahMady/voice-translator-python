from googletrans import Translator
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # calibrate mic
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')  # change if Arabic
        print(f"You Said: {query}\n")

    except Exception as e: 
        print("Error:", e)
        print("Say that again Please...")
        speak("Say that again Please...")
        return "None"

    return query


def Translate():
	speak("what I should Translate??")
	sentence = takeCommand()
	trans = Translator()
	trans_sen = trans.translate(sentence,src='en',dest='ca')
	print(trans_sen.text)
	speak(trans_sen.text)

Translate()
