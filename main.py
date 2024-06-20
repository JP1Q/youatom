from whisper import load_model, pad_or_trim, log_mel_spectrogram, decode
import whisper
import requests
import os
# import keyboard
# import time
from pytube import YouTube

def get_audio_youtube(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    filename = "recorded_audio.mp3"
    audio_stream.download(filename=filename)


def get_ai_response(prompt):
    prompt = "Generate atomic notes, add some stuff if you know something about it, they might be showing some examples try to guess them and show them, from the following text write it in mark down format the text is as follows: " + prompt
    # os.system('clear')
    print("AI HAS BEEN GIVEN THIS PROMPT:")
    print(prompt)
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print("Error:", e)
        return None

def clear():
    try:
        os.system('clear')
    except:
        os.system('cls')

def transcribe_audio(audio_file):
    # Load Whisper model
    model = whisper.load_model("base")
    result = ""
    print("Transcribing")
    try:
        result = whisper.transcribe(audio=audio_file, model=model)

    except Exception as e:
        print(f"Error processing audio file: {e}")

    print(result["text"])
    return result["text"]

if __name__ == "__main__":

    print("Welcome to youtranscript")
    url = input("Please input the youtube url: ")
    get_audio_youtube(url)
    clear()


    # Specify the path where the recorded audio will be saved
    output_audio_file = "recorded_audio.mp3"  # You can change the format to MP3 or other supported formats


    # Transcribe the recorded audio using Whisper
    print("PROCESSING WITH AI.. PLEASE WAIT A MOMENT")

    print("GETTING TRANSCRIPTION")
    print()
    transcription = transcribe_audio(output_audio_file)
    clear()
    print("GETTING AI OUTPUT")
    print()
    # Process the transcription with AI
    ai_out = get_ai_response(transcription)
    if ai_out:
        print(ai_out["response"])
    else:
        print("AI response not available")
