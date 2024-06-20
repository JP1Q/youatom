# youatom

## What does it do?
You simply input a youtube url and it spit's out atomic notes of the video

## How does it work?
Using dash, openai-whisper and llama3

## Why does this exist?
Because I don't have time to watch 2 hour videos on youtube which are supposed to teach me something

## Pre installation:
Make sure you have ollama installed via:
```
curl -fsSL https://ollama.com/install.sh | sh
```

Make sure that you have llama3 installed via:
```
ollama run llama3
/bye
```

Make sure that you have the ollama api running by:
```
ollama serve
```
(do not worry if it says that the port is already in use, since its probably already used by ollama it self)


## Installation:
```
git clone https://github.com/JP1Q/youatom
cd youatom
pip install -r requirements.txt
```

## Runing the app:

To run the website use:
```
python main_dash.py
```

To run the tkinter app use:
```
python main_tk.py
```

To run the cli app use:
```
python main.py
```

