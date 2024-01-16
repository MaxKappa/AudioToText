from pydub import AudioSegment
import logging
import os

class AudioFileManager:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_formats = ['wav'] 
        self.setup_logger()

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def upload_audio_file(self, uploaded_file):
        try:
            file_format = self._get_file_format(uploaded_file)
            file_path = os.path.join(self.input_dir, uploaded_file)

            if file_format not in self.supported_formats:
                converted_file_path = self._convert_to_supported_format(file_path, file_format)
                return converted_file_path  
            else:
                self.save_audio_file(uploaded_file, uploaded_file)
                return file_path 
        except Exception as e:
            self.logger.error(f"Errore nel caricamento del file: {e}")
            raise

    def save_chunk(self, chunk, file_name):
        with open(os.path.join(self.output_dir, file_name), 'a') as file:
            file.write(chunk)
        

    def _convert_to_supported_format(self, file_path, original_format):
        try:
            audio = AudioSegment.from_file(file_path, format=original_format)
            converted_file_path = file_path.rsplit('.', 1)[0] + '.wav'
            audio.export(converted_file_path, format='wav')
            self.logger.info(f"File convertito in formato WAV: {converted_file_path}")
            return converted_file_path
        except Exception as e:
            self.logger.error(f"Errore nella conversione del file: {e}")
            raise
    def _get_file_format(self, file):
        return file.split('.')[-1]


