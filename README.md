# Audio Recorder and Transcription using AssemblyAI

This project demonstrates how to record audio, upload it to AssemblyAI for transcription, and save the transcribed text locally. The project leverages `sounddevice` for recording audio and `requests` for handling HTTP requests to the AssemblyAI API.

## Features

- Record audio from the microphone
- Upload recorded audio to AssemblyAI
- Transcribe audio using AssemblyAI's API
- Save the transcription result to a text file

## Prerequisites

- Python 3.6 or higher
- AssemblyAI API key

![hi](https://github.com/user-attachments/assets/b25e6227-0d40-428e-84c1-47ee3251e2b7)


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/PiyushKumar-30/Voice-Recognition-Project
    cd Voice-Recognition-Project
    ```

2. Set your AssemblyAI API key:
    Replace the `API_KEY_ASSEMBLYAI` value in the script with your actual AssemblyAI API key.

## Usage

1. Run the script:
    ```sh
    python voice_recognition.py
    ```

2. The script will:
    - Record 5 seconds of audio and save it as `output.wav`.
    - Upload the recorded audio to AssemblyAI.
    - Transcribe the uploaded audio.
    - Save the transcription result to a text file named `transcript.txt`.

## Project Structure

- `voice_recognition.py`  :   Main script for recording and transcribing audio <br />
- `README.md` :               This README file

## Example

Here's an example of what you can expect in the terminal output:  <br />
INFO - Recording audio... <br />
INFO - Audio recording saved as output.wav <br />
INFO - Starting the transcription process... <br />
INFO - Waiting for 30 seconds before polling again... <br />
INFO - Transcript saved <br />



The transcription result will be saved in a file named `transcript.txt`.

## Dependencies

- `sounddevice`: For recording audio
- `scipy`: For writing audio files
- `requests`: For making HTTP requests
- `logging`: For logging information and errors

Install these dependencies using:
```sh
pip install sounddevice scipy requests
```

## Acknowledgments
Thanks to AssemblyAI for providing the API for audio transcription.

