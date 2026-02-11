import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import arabic_reshaper
from bidi.algorithm import get_display

# --- 1. SETTINGS & LANGUAGE SELECTION ---
def select_language():
    print("\n--- Select Language / Choose Language ---")
    print("1. Speak English -> Translate to Arabic")
    print("2. Speak Arabic  -> Translate to English")
    choice = input("Enter number (1 or 2): ")
    
    if choice == '2':
        # You speak Arabic, it translates to English
        return 'ar-SA', 'en' 
    else:
        # Default: You speak English, it translates to Arabic
        return 'en-US', 'ar'

# Run detection immediately
INPUT_LANG, TARGET_LANG = select_language()
print(f"[+] Configured: Speaking {INPUT_LANG} -> Translating to {TARGET_LANG}\n")

# --- 2. DISPLAY HELPER (Fixes Arabic visual bugs) ---
def get_visually_correct_text(text):
    if text is None:
        return ""
    # Only fix if the text contains Arabic characters
    if any("\u0600" <= char <= "\u06FF" for char in text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    return text

# --- 3. SPEAK FUNCTION (High Quality Google Voice) ---
def speak(text, lang):
    # Fix display before printing
    display_text = get_visually_correct_text(text)
    print(f"[Speaker] ({lang}): {display_text}")

    try:
        # Generate audio file
        tts = gTTS(text=text, lang=lang)
        filename = "voice_output.mp3"
        
        # Clean up old file
        if os.path.exists(filename):
            os.remove(filename)
            
        # Save and Play
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
        
    except Exception as e:
        print(f"[!] Audio Error: {e}")

# --- 4. LISTENING FUNCTION ---
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[*] Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("[*] Recognizing...")
            # Uses the selected INPUT_LANG
            query = r.recognize_google(audio, language=INPUT_LANG)
            
            # Fix display in case user spoke Arabic
            display_query = get_visually_correct_text(query)
            print(f"[>] You Said: {display_query}\n")
            return query
        except Exception as e:
            print("[!] Error:", e)
            return None

# --- 5. MAIN LOGIC ---
def Translate():
    # Prompt the user to start
    print("[*] Ready. Start speaking now.")
    
    sentence = takeCommand()
    
    if sentence is None:
        return

    translator = Translator()
    try:
        # Translate to the target language
        translated = translator.translate(sentence, src='auto', dest=TARGET_LANG)
        final_text = translated.text
        
        # A. Show it in terminal (Fixed View)
        fixed_text = get_visually_correct_text(final_text)
        print(f"[=] Translation: {fixed_text}")
        
        # B. Save it to file
        with open("translation_result.txt", "w", encoding="utf-8") as f:
            f.write(final_text)
        print("[+] Saved to: translation_result.txt")

        # C. Speak it
        speak(final_text, TARGET_LANG)
        
    except Exception as e:
        print(f"[!] Translation Failed: {e}")
        speak("Sorry, something went wrong.", 'en')

if __name__ == "__main__":
    Translate()