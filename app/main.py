# main.py
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from utils.audioFileManager import AudioFileManager
from utils.audioTranscriber import AudioTranscriber
import threading

# Inizializzazione dell'app Flask e configurazione
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['TRANSCRIPTION_FOLDER'] = 'transcriptions/'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'mp4'}
audio_manager = AudioFileManager(app.config['UPLOAD_FOLDER'], app.config['TRANSCRIPTION_FOLDER'])
transcriber = AudioTranscriber(audio_manager)

# Funzione helper per controllare se il file è consentito
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Endpoint della pagina iniziale
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint per il caricamento dei file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return redirect(url_for('index'))
    file = request.files['audioFile']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))
    
    # Salvataggio del file caricato
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Avvio della trascrizione in un thread separato
    output_filename = filename.rsplit('.', 1)[0] + '.txt'
    transcription_thread = threading.Thread(target=transcribe_audio, args=(file_path, output_filename))
    transcription_thread.start()

    return render_template('loading.html', filename=output_filename)

# Funzione per la trascrizione
def transcribe_audio(file_path, output_filename):
    transcriber.transcribe(file_path, output_filename)

# Endpoint per il download della trascrizione
@app.route('/download/<filename>')
def download_transcription(filename):
    return send_from_directory(app.config['TRANSCRIPTION_FOLDER'], filename)


app.run(host='localhost', port=8181, debug=True)