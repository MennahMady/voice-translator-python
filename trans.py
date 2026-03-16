import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
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
        return 'ar-SA', 'en', "Helsinki-NLP/opus-mt-ar-en" 
    else:
        return 'en-US', 'ar', "Helsinki-NLP/opus-mt-en-ar"

INPUT_LANG, TARGET_LANG, MODEL_NAME = select_language()
print(f"Configured: Speaking {INPUT_LANG} -> Translating to {TARGET_LANG}\n")

# --- 2. INITIALIZE LOCAL ML MODEL (The Proper Way) ---
print("Loading local Tokenizer and Model... (Downloading weights if first run)")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully into memory!\n")

# --- 3. DISPLAY HELPER ---
def get_visually_correct_text(text):
    if text is None:
        return ""
    if any("\u0600" <= char <= "\u06FF" for char in text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    return text

# --- 4. SPEAK FUNCTION ---
def speak(text, lang):
    display_text = get_visually_correct_text(text)
    print(f"[Speaker] ({lang}): {display_text}")
    try:
        tts = gTTS(text=text, lang=lang)
        filename = "voice_output.mp3"
        if os.path.exists(filename):
            os.remove(filename)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Audio Error: {e}")

# --- 5. LISTENING FUNCTION ---
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language=INPUT_LANG)
            display_query = get_visually_correct_text(query)
            print(f"You Said: {display_query}\n")
            return query
        except Exception as e:
            print("Error:", e)
            return None

# --- 6. MAIN LOGIC ---
def Translate():
    print("Ready. Start speaking now.")
    sentence = takeCommand()
    
    if sentence is None:
        return

    try:
        # Run local ML inference directly!
        print("Translating via local tensors...")
        inputs = tokenizer(sentence, return_tensors="pt", padding=True)
        translated_tokens = model.generate(**inputs)
        final_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        
        fixed_text = get_visually_correct_text(final_text)
        print(f"Translation: {fixed_text}")
        
        with open("translation_result.txt", "w", encoding="utf-8") as f:
            f.write(final_text)
        print("Saved to: translation_result.txt")

        speak(final_text, TARGET_LANG)
        
    except Exception as e:
        print(f"Translation Failed: {e}")
        speak("Sorry, something went wrong.", 'en')

if __name__ == "__main__":
    Translate()