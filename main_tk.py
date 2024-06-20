import os
import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from whisper import load_model, transcribe
import requests
import webbrowser
import threading


class YouTubeTranscriptApp:
    def __init__(self, master):
        self.master = master
        master.title("Youscript")

        self.label = tk.Label(master, text="Enter YouTube URL:")
        self.label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_process)
        self.start_button.pack()

        self.progress_label = tk.Label(master, text="")
        self.progress_label.pack()

        self.progressbar = ttk.Progressbar(master, orient="horizontal", mode="indeterminate")
        self.progressbar.pack()

        self.transcription = None

    def start_process(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Error", "Please enter a YouTube URL.")
            return

        # Disable start button and enable progress bar
        self.start_button.config(state=tk.DISABLED)
        self.progressbar.start()

        # Start a thread for downloading and processing
        threading.Thread(target=self.process_audio, args=(url,), daemon=True).start()

    def process_audio(self, url):
        try:
            # Download audio from YouTube
            self.update_progress("Downloading audio...")
            audio_file = self.download_audio(url)

            # Transcribe audio using Whisper
            self.update_progress("Transcribing audio...")
            transcription = self.transcribe_audio(audio_file)

            # Get AI response
            self.update_progress("Getting AI response...")
            ai_response = self.get_ai_response(transcription)

            # Open AI response in a markdown window
            self.open_markdown_window(ai_response)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            # Reset UI after processing
            self.progressbar.stop()
            self.progress_label.config(text="")
            self.start_button.config(state=tk.NORMAL)

    def download_audio(self, url):
        try:
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            filename = "recorded_audio.mp3"
            audio_stream.download(filename=filename)
            return filename
        except Exception as e:
            raise RuntimeError(f"Error downloading audio: {e}")

    def transcribe_audio(self, audio_file):
        try:
            model = load_model("base")
            result = transcribe(audio=audio_file, model=model)
            return result["text"]
        except Exception as e:
            raise RuntimeError(f"Error transcribing audio: {e}")

    def get_ai_response(self, prompt):
        prompt = "Generate atomic notes, add some stuff if you know something about it, they might be showing some examples try to guess them and show them, from the following text write it in mark down format the text is as follows: " + prompt
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            return response.json()["response"]
        except Exception as e:
            raise RuntimeError(f"Error getting AI response: {e}")

    def open_markdown_window(self, ai_response):
        self.transcription = ai_response
        markdown_window = tk.Toplevel(self.master)
        markdown_window.title("AI Response in Markdown")
        markdown_text = tk.Text(markdown_window, wrap="word")
        markdown_text.pack(fill="both", expand=True)
        markdown_text.insert("1.0", ai_response)

        def open_in_browser():
            html_content = f"<html><body>{ai_response}</body></html>"
            with open("ai_response.html", "w", encoding="utf-8") as file:
                file.write(html_content)
            webbrowser.open("file://" + os.path.realpath("ai_response.html"))

        open_browser_button = tk.Button(markdown_window, text="Open in Browser", command=open_in_browser)
        open_browser_button.pack()

    def update_progress(self, message):
        self.progress_label.config(text=message)
        self.master.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeTranscriptApp(root)
    root.mainloop()
