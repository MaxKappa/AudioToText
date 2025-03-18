# AudioToText

AudioToText is a web-based application that leverages OpenAI's Whisper model for efficient and accurate audio-to-text transcription. It allows users to upload audio files and receive textual transcriptions, making it highly useful for transcribing interviews, lectures, meetings, and other audio recordings.

## Features
- Audio File Upload: Supports various formats including MP3, WAV, MP4, M4A.
- Automatic Transcription: Utilizes OpenAI's Whisper model for high-accuracy audio-to-text conversion.
- Transcription Download: Enables users to download the transcribed text file.

Getting Started
## Prerequisites
- Python 3.6 or later.
- Flask
- OpenAI's Whisper model.

## Installation
Clone the repository:
```
git clone https://github.com/MaxKappa/AudioToText.git
```
Install dependencies:
```
cd AudioToText
pip install -r requirements.txt
```

Run the application:
```
python main.py
```

The application will be accessible at localhost:8181.

## Usage
Navigate to the application: Open your web browser and go to http://localhost:8181.
Upload an audio file: Follow the instructions on the web interface to upload your audio file.
Wait for transcription: The application will transcribe the audio using OpenAI's Whisper model. You can monitor the progress on the interface.
Download the transcription: Once the transcription is complete, download the text file from the provided link.

## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to OpenAI for developing the Whisper model.
