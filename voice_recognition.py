import sounddevice as sd
from scipy.io.wavfile import write
import requests
import time
import logging
import os

# Replace with your actual API key from AssemblyAI
API_KEY_ASSEMBLYAI = "a12244c38482483d9b9de4b99dd8aeec"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AssemblyAI API endpoints
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

# Headers for requests
headers_auth_only = {'authorization': API_KEY_ASSEMBLYAI}
headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

# Chunk size for uploading in bytes (5MB)
CHUNK_SIZE = 5_242_880

# Function to record audio
def record_audio(filename, duration=5, freq=44100):
    logging.info("Recording audio...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write(filename, freq, recording)
    logging.info(f"Audio recording saved as {filename}")

# Function to upload audio file
def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    try:
        upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
        upload_response.raise_for_status()
        return upload_response.json()['upload_url']
    except requests.RequestException as e:
        logging.error(f"Failed to upload file: {e}")
        return None

# Function to transcribe audio
def transcribe(audio_url):
    transcript_request = {
        'audio_url': audio_url
    }

    try:
        transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
        transcript_response.raise_for_status()
        return transcript_response.json()['id']
    except requests.RequestException as e:
        logging.error(f"Failed to initiate transcription: {e}")
        return None

# Function to poll transcription status
def poll(transcript_id):
    polling_endpoint = f"{transcript_endpoint}/{transcript_id}"
    try:
        polling_response = requests.get(polling_endpoint, headers=headers)
        polling_response.raise_for_status()
        return polling_response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to poll transcription status: {e}")
        return None

# Function to get transcription result
def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    if not transcribe_id:
        return None, "Failed to transcribe"

    while True:
        data = poll(transcribe_id)
        if not data:
            return None, "Polling error"

        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']

        logging.info("Waiting for 30 seconds before polling again...")
        time.sleep(30)

# Function to save transcript
def save_transcript(url, title):
    data, error = get_transcription_result_url(url)

    if data:
        filename = f"{title}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(data['text'])
            logging.info('Transcript saved')
        except IOError as e:
            logging.error(f"Failed to save transcript: {e}")
    elif error:
        logging.error(f"Error: {error}")

# Main function to combine recording and transcribing
if __name__ == "__main__":
    audio_filename = "output.wav"  # File to save the recorded audio
    transcript_title = "transcript"  # Desired title for the transcript

    # Record audio
    record_audio(audio_filename, duration=10)

    # Upload and transcribe the recorded audio
    logging.info("Starting the transcription process...")
    audio_url = upload(audio_filename)
    if audio_url:
        save_transcript(audio_url, transcript_title)
    else:
        logging.error("Failed to upload the audio file.")
