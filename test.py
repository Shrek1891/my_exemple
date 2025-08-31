from io import BytesIO

from gtts import gTTS

mp3_fp = BytesIO()

text = 'hello'
tts = gTTS('hello', lang='en')
tts.write_to_fp(mp3_fp)