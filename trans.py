from googletrans import Translator
import pyttsx3
import speech_recognition as sr

# --- Setup Voice ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Try to set a voice (Index 1 is usually a 2nd voice, Index 0 is default)
try:
    engine.setProperty('voice', voices[1].id)
except:
    engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("⏳ Recognizing...")
            # Use 'en-US' for English input
            query = r.recognize_google(audio, language='en-US')
            print(f"✅ You Said: {query}\n")
        except Exception as e:
            print("❌ Error:", e)
            return "None"

    return query

def Translate():
    speak("What should I Translate?")
    sentence = takeCommand()
    
    if sentence == "None":
        speak("I didn't hear you.")
        return

    trans = Translator()
    
    # --- THIS WAS THE FIX ---
    # Changed dest='ca' (Catalan) to dest='ar' (Arabic)
    try:
        trans_sen = trans.translate(sentence, src='en', dest='ar')
        
        print(f"📝 Arabic Translation: {trans_sen.text}")
        
        # Note: This might not speak correctly if you don't have an Arabic voice installed
        speak(trans_sen.text)
        
    except Exception as e:
        print("Translation Error:", e)
        speak("Sorry, the translation failed.")

if __name__ == "__main__":
    Translate()