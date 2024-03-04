from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
from gtts import gTTS
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def pdf_to_text(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def text_to_speech(text, output_folder):
    output_path = os.path.join(output_folder, 'output.mp3')  # Use a fixed name for the audio file
    tts = gTTS(text, lang='en')
    tts.save(output_path)
    # Replace backward slashes with forward slashes in the URL
    return output_path.replace('\\', '/')

@app.route('/convert', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file has a valid extension
        if file and file.filename.endswith('.pdf'):
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Convert PDF to text
            text = pdf_to_text(pdf_path)

            # Convert text to speech
            output_folder = app.config['UPLOAD_FOLDER']
            output_path = text_to_speech(text, output_folder)

            # Provide a link to download the audio file
            return render_template('detect.html', audio_url=output_path)

    return render_template('detect.html', audio_url=None)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
