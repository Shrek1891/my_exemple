import langid
morze_dict = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": "/"
}

allowed_chars = set(morze_dict.keys())

def is_valid_morze(text):
    for char in text:
        if char.lower() not in allowed_chars and char != ' ':
            return False
    return True

def to_morze(text):
    morze_text = ""
    for char in text.lower():
        if char in morze_dict:
            morze_text += morze_dict[char] + " "
        else:
            morze_text += "? "  # For characters not in the dictionary
    return morze_text.strip()

def from_morze(morze_text):
    text = ""
    for code in morze_text.split():
        for char, morze in morze_dict.items():
            if morze == code:
                text += char
                break
        else:
            text += "?"  # For morze codes not in the dictionary
    return text

def detect_language(text):
    try:
        lang = langid.classify(text)
        print(f"Detected language: {lang[0]}")
        return lang[0]
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "unknown"


def convert(type, morze_text,is_error,is_success ):
    error_message = ""
    if type == 'Translate to morze':
        checked_lang = detect_language(morze_text)
        if checked_lang != 'en' and checked_lang != 'it' and checked_lang != 'fr' and checked_lang != 'de':
            is_error = True
            error_message = "Please enter text in English."
        else:
            is_success = True
            morze_text = to_morze(morze_text)
    if type == 'Translate from morze':
        if is_valid_morze(morze_text):
            is_error = True
            error_message = "Please enter morze code."
        else:
            is_success = True
            morze_text = from_morze(morze_text)
    return morze_text, is_error, error_message, is_success

