import re
from io import BytesIO
from PyPDF2 import PdfReader
from flask import Flask, render_template, request, send_file, redirect, session, make_response
from audioBook import convert_pdf_to_text, get_language, check_file_is_pdf, get_first_sentence, get_audio_from_text
from constants import MENU, MENU_PROJECTS, MORZE_MENU, WATERMARK_MENU, TIC_TAC_TOE_MENU, SPEED_TYPING_MENU
from morze import convert
from constants import PROJECTS

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'super secret key'


@app.route('/')
def index():
    url = request.url
    return render_template('home.html', menu=MENU)


@app.route('/projects')
def projects():
    url = request.url
    return render_template('projects.html', menu=MENU, projects=PROJECTS)


@app.route('/projects/morze', methods=['GET', 'POST'])
def project_morze(project_name='morze'):
    is_error = False
    error_message = ""
    is_success = False
    if request.method == 'POST':
        morze_text = request.form.get('morze_text').strip()
        type = request.form.get('translateType')
        morze_text, is_error, error_message, is_success = convert(type, morze_text, is_error, is_success)
        return render_template(
            f'/projects/morze.html',
            menu=MORZE_MENU,
            project_name=project_name,
            morze_text=morze_text,
            is_error=is_error,
            error_message=error_message,
            is_success=is_success
        )
    else:
        return render_template(
            f'/projects/morze.html',
            menu=MENU_PROJECTS,
            project_name=project_name,
            is_error=is_error,
            error_message=error_message,
        )


@app.route('/projects/watermark', methods=['GET', 'POST'])
def project_watermark():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            from water_mark import wartermark_image
            watermark_text = request.form['watermark_text']
            water_marked_image = wartermark_image(image, watermark_text)
            water_marked_image.save("static/watermarked_image.jpg", "JPEG")
        return render_template(
            '/projects/watermark.html',
            menu=WATERMARK_MENU,
            is_success=True, )
    return render_template('/projects/watermark.html', menu=MENU_PROJECTS)


@app.route('/projects/watermark/get_image')
def get_image():
    return send_file("static/watermarked_image.jpg", mimetype='image/jpeg')


@app.route('/projects/tic-tac-toe')
def project_tic_tac_toe():
    return render_template('/projects/tic-tac-toe.html', menu=MENU_PROJECTS)


@app.route('/projects/tic-tac-toe/play')
def tic_tac_toe():
    return render_template('/projects/tic-tac-toe_play.html', menu=TIC_TAC_TOE_MENU)


@app.route('/projects/speed-typing')
def project_speed_typing():
    return render_template('/projects/speed-typing.html', menu=MENU_PROJECTS)


@app.route('/projects/speed-typing/play')
def speed_typing():
    return render_template('/projects/speed-typing-play.html', menu=SPEED_TYPING_MENU)


@app.route('/projects/game')
def game():
    return render_template('projects/game.html', menu=MENU_PROJECTS)


@app.route('/projects/game/play')
def game_play():
    return render_template('projects/game_play.html', menu=MENU_PROJECTS)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', menu=MENU)


pdf_data = None
text = None
audio = None
sentences = None
lang = None


@app.route('/projects/audio-book', methods=['GET', 'POST'])
def audio_book():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if not check_file_is_pdf(pdf_file) or not pdf_file:
            return render_template(
                'projects/audioBook.html',
                menu=MENU_PROJECTS,
                is_error=True,
                error_message='Please upload PDF file'
            )
        global text, pdf_data
        pdf_data = BytesIO(pdf_file.read())
        return redirect('/projects/audio-book/play')
    return render_template('projects/audioBook.html', menu=MENU_PROJECTS)


@app.route('/projects/audio-book/play')
def audio_book_play():
    global audio, lang, sentences
    text = ''
    length = len(PdfReader(pdf_data).pages)
    for i in range(length):
        page = PdfReader(pdf_data).pages[i]
        text += page.extract_text()
    first_sentence = get_first_sentence(text)
    sentences = re.split(r'(?<!\w\同)\.\s(?!\w\同)', text)
    lang = get_language(first_sentence)
    session['index'] = 0
    return render_template('projects/audioBook_play.html', menu={'back': {'name': 'back', 'url': '/projects/audio-book'}}, text=text)


@app.route('/projects/audio-book/get_audio')
def get_audio():
    global audio
    if session['index'] >= len(sentences) - 1:
        session['index'] = 0
    audio = get_audio_from_text(sentences[session['index']], lang)
    session['index'] += 1
    return send_file('static/audio.mp3', mimetype='audio/mpeg', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
