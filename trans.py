from googletrans import Translator
import pyttsx3
import speech_recognition as sr

# --- NEW IMPORTS FOR ARABIC FIX ---
import arabic_reshaper
from bidi.algorithm import get_display

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

try:
    engine.setProperty('voice', voices[1].id)
except:
    engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# --- HELPER FUNCTION TO FIX ARABIC DISPLAY ---
def print_ar(text):
    # 1. Reshape connects the letters (isolated -> connected)
    reshaped_text = arabic_reshaper.reshape(text)
    # 2. bidi flips it to Right-to-Left
    bidi_text = get_display(reshaped_text)
    print(bidi_text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("⏳ Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(f"✅ You Said: {query}\n")
        except Exception as e:
            print("❌ Error:", e)
            return "None"

    return query

def Translate():
    speak("What should I translate?")
    sentence = takeCommand()
    
    if sentence == "None":
        speak("I didn't hear you.")
        return

    trans = Translator()
    
    try:
        # Translating to Arabic ('ar')
        trans_sen = trans.translate(sentence, src='en', dest='ar')
        
        # --- USE THE FIX HERE ---
        print("📝 Translation (Corrected View):")
        print_ar(trans_sen.text) 
        
        # Note: 'speak' might still struggle with Arabic audio if no Arabic voice is installed
        speak(trans_sen.text)
        
    except Exception as e:
        print("Translation Error:", e)
        speak("Sorry, the translation failed.")

if __name__ == "__main__":
    Translate()