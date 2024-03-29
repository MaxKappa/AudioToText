import whisper
import logging
from pydub import AudioSegment
import time
import os
import threading

class AudioTranscriber:
    def __init__(self, audio_file_manager, model_name='small'):
        self.model = whisper.load_model(model_name, device="cpu")
        self.setup_logger()
        self.chunk_length_ms = 120000
        self.audio_file_manager = audio_file_manager
        self.remaining_time = 0
        self.time_lock = threading.Lock()
        self.estimated_total_time = 0

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def transcribe(self, audio_path, output_file_name):
        try:
            audio = AudioSegment.from_file(audio_path)
            chunks = self._split_into_chunks(audio)
            transcriptions = []
            start_time = time.time()
            for i, chunk in enumerate(chunks):
                chunk.export("temp_chunk.wav", format="wav")
                result = self.model.transcribe("temp_chunk.wav", fp16=False, language="Italian")
                transcriptions.append(result['text'])
                elapsed_time = time.time() - start_time
                with self.time_lock:
                    self.estimated_total_time = elapsed_time / (i + 1) * len(chunks)
                with self.time_lock:
                    self.remaining_time = self.estimated_total_time - elapsed_time
                self.audio_file_manager.save_chunk(result["text"], output_file_name)
                self.logger.info(f"Chunk {i+1}/{len(chunks)} trascritto. Tempo rimanente stimato: {self.remaining_time:.2f} secondi")
            os.remove("temp_chunk.wav")
            return ' '.join(transcriptions)
        except Exception as e:
            self.logger.error(f"Errore nella trascrizione del file {audio_path}: {e}")
            raise
    
    def getRemainingTime(self):
        with self.time_lock:
            return int(self.remaining_time)

    def getEstimatedTotalTime(self):
        with self.time_lock:
            return int(self.estimated_total_time)
    def _split_into_chunks(self, audio):
        return [audio[i:i + self.chunk_length_ms] for i in range(0, len(audio), self.chunk_length_ms)]

