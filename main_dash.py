import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
from pytube import YouTube
from whisper import load_model, transcribe

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom HTML and CSS for black-and-white theme and custom font
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet">
        <style>
            body {
                background-color: black;
                color: white;
                font-family: 'JetBrains Mono', monospace;
            }
            .card {
                border: 1px solid white;
                background-color: black;
                color: white;
            }
            .btn-primary {
                background-color: white;
                color: black;
                border-color: white;
            }
            .input-group-text {
                background-color: black;
                color: white;
                border: 1px solid white;
            }
            .form-control {
                background-color: black;
                color: white;
                border: 1px solid white;
            }
            ::placeholder {
                color: red;
            }
            pre {
                border: 1px solid white;
                padding: 10px;
                overflow-x: auto;
                font-family: 'JetBrains Mono', monospace;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Youscript"),
                width=12,
                className="text-center"
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Enter YouTube URL:"),
                            dbc.Input(id="url-input", type="text", placeholder="https://www.youtube.com/..."),
                        ]
                    ),
                    width=12,
                    md=10,
                    lg=8,
                    className="mb-2 mx-auto"
                ),
                dbc.Col(
                    dbc.Button("Start", id="start-button", color="primary", className="btn-block"),
                    width=12,
                    md=2,
                    lg=2,
                    className="mx-auto"
                ),
            ],
            className="my-3",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Markdown(id="output", style={"white-space": "pre-wrap"})
                    ),
                    className="mt-3"
                ),
                width=12,
                md=10,
                lg=8,
                className="mx-auto"
            ),
        ),
    ],
    fluid=True,
)

@app.callback(
    [
        Output("output", "children"),
        Output("start-button", "disabled"),
    ],
    [Input("start-button", "n_clicks")],
    [State("url-input", "value")]
)
def start_process(n_clicks, url):
    if n_clicks is None or not url:
        return "", False

    def update_progress(message):
        return message, True

    try:
        # Update progress
        progress_message, button_disabled = update_progress("Downloading audio...")

        # Download audio from YouTube
        audio_file = download_audio(url)
        
        # Update progress
        progress_message, button_disabled = update_progress("Transcribing audio...")

        # Transcribe audio using Whisper
        transcription = transcribe_audio(audio_file)

        # Update progress
        progress_message, button_disabled = update_progress("Getting AI response...")

        # Get AI response
        ai_response = get_ai_response(transcription)

        return ai_response, False

    except Exception as e:
        return f"An error occurred: {e}", False

def download_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = "recorded_audio.mp3"
        audio_stream.download(filename=filename)
        return filename
    except Exception as e:
        raise RuntimeError(f"Error downloading audio: {e}")

def transcribe_audio(audio_file):
    try:
        model = load_model("base")
        result = transcribe(audio=audio_file, model=model)
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Error transcribing audio: {e}")

def get_ai_response(prompt):
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

if __name__ == "__main__":
    app.run_server(debug=True)
