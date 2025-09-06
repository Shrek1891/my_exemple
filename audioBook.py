from io import BytesIO

from PyPDF2 import PdfReader


def convert_pdf_to_text(data):
    text = ''
    pdf_data = BytesIO(data.read())
    reader = PdfReader(pdf_data)
    for page in reader.pages:
        text += page.extract_text()
    return text


def get_first_sentence(text):
    try:
        dot_index = text.index(".")
        return text[:dot_index + 1]
    except ValueError:
        return text



def get_language(text):
    import langid
    return langid.classify(text)[0]


def check_file_is_pdf(file):
    return file.filename.endswith('.pdf')

def get_audio_from_text(text,lang):
    from gtts import gTTS
    mp3_fp = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fp)
    tts.save('static/audio.mp3')
    return mp3_fp

if __name__ == '__main__':
    pass
