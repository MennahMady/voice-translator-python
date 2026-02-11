from deep_translator import GoogleTranslator
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic_display(text):
    # Reshape connects the letters correctly
    reshaped_text = arabic_reshaper.reshape(text)
    # get_display fixes the Right-to-Left direction
    bidi_text = get_display(reshaped_text)
    return bidi_text

text_to_translate = input("Enter something to translate: ")

translator = GoogleTranslator(source='auto', target='ar')
translated_text = translator.translate(text_to_translate)

# Fix the look for the console
display_text = fix_arabic_display(translated_text)

print(f"Translated (Fixed View): {display_text}")