import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import arabic_reshaper
from bidi.algorithm import get_display

# --- 1. SETTINGS & LANGUAGE SELECTION ---
def select_language():
    print("\n--- Select Language / اختر اللغة ---")
    print("1. English (Speak English -> Translate to Arabic)")
    print("2. Arabic  (Speak Arabic  -> Translate to English)")
    choice = input("Enter number (1 or 2): ")
    
    if choice == '2':
        # You speak Arabic ('ar-SA'), it translates to English ('en')
        return 'ar-SA', 'en' 
    else:
        # Default: You speak English ('en-US'), it translates to Arabic ('ar')
        return 'en-US', 'ar'

# Run this function immediately to set the global variables
INPUT_LANG, TARGET_LANG = select_language()

print(f"Configured: Speaking {INPUT_LANG} -> Translating to {TARGET_LANG}\n")

# --- 2. SPEAK FUNCTION (High Quality Google Voice) ---
def speak(text, lang='en'):
    #print(f"Speaking ({lang}): {text}")
    try:
        # Generate audio file from Google
        tts = gTTS(text=text, lang=lang)
        filename = "voice_output.mp3"
        
        # Remove old file if it exists (prevents permission errors)
        if os.path.exists(filename):
            os.remove(filename)
            
        # Save and Play
        tts.save(filename)
        playsound(filename)
        
        # Clean up
        os.remove(filename)
        
    except Exception as e:
        print(f"Audio Error: {e}")

# --- 3. DISPLAY HELPER (Fixes Arabic visual bugs) ---
def print_corrected_arabic(text):
    # Reshape: Connects letters (e.g., م + ر -> مر)
    reshaped_text = arabic_reshaper.reshape(text)
    # Bidi: Reverses direction (Right-to-Left)
    bidi_text = get_display(reshaped_text)
    print(f"Translation (Terminal View): {bidi_text}")

# --- 4. LISTENING FUNCTION ---
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Calibrate mic for noise
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language=INPUT_LANG)
            print(f"You Said: {query}\n")
            return query
        except Exception as e:
            print("Error:", e)
            return None

# --- 5. MAIN LOGIC ---
def Translate():
    # Ask user for input
    speak("What should I translate?", 'en')
    
    sentence = takeCommand()
    
    if sentence is None:
        speak("I didn't hear anything.", 'en')
        return

    # Translate
    translator = Translator()
    try:
        translated = translator.translate(sentence, src='en', dest=TARGET_LANG)
        arabic_text = translated.text
        
        # A. Show it in terminal (Best effort)
        print_corrected_arabic(arabic_text)
        
        # B. Save it to file (Perfect proof)
        with open("translation_result.txt", "w", encoding="utf-8") as f:
            f.write(arabic_text)
        print("Saved perfect text to: translation_result.txt")

        # C. Speak it (Perfect audio)
        speak(arabic_text, TARGET_LANG)
        
    except Exception as e:
        print(f"Translation Failed: {e}")
        speak("Sorry, something went wrong.", 'en')

if __name__ == "__main__":
    Translate()