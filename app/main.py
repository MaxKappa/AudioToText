# main.py
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from utils.audioFileManager import AudioFileManager
from utils.audioTranscriber import AudioTranscriber
import threading


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['TRANSCRIPTION_FOLDER'] = 'transcriptions/'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'mp4', 'm4a'}
audio_manager = AudioFileManager(app.config['UPLOAD_FOLDER'], app.config['TRANSCRIPTION_FOLDER'])
transcriber = AudioTranscriber(audio_manager)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return redirect(url_for('index'))
    file = request.files['audioFile']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    output_filename = filename.rsplit('.', 1)[0] + '.txt'
    transcription_thread = threading.Thread(target=transcribe_audio, args=(file_path, output_filename))
    transcription_thread.start()

    return render_template('loading.html', filename=output_filename)

def transcribe_audio(file_path, output_filename):
    transcriber.transcribe(file_path, output_filename)

@app.route('/download/<filename>')
def download_transcription(filename):
    file_path = os.path.join(app.config['TRANSCRIPTION_FOLDER'], filename)
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/remaining-time')
def remaining_time():
    return jsonify({"remainingTime": str(transcriber.getRemainingTime()), "estimatedTotalTime": str(transcriber.getEstimatedTotalTime())})


if __name__ == '__main__':
    app.run(host='localhost', port=8181, debug=True)