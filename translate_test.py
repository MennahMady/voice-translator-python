from googletrans import Translator

translator = Translator()

text = input("Enter something to translate: ")

result = translator.translate(text, src='en', dest='ar')

print("Translated text:", result.text)
