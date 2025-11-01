🧠 Jarvis – Your Personal AI Voice Assistant

Jarvis is a voice-controlled personal assistant built in Python that listens to your commands, speaks naturally, and performs a variety of everyday tasks — all powered by Google Gemini AI and open-source tools.

🚀 Features

🎙️ Always Listening – Activates with the wake word “Jarvis” and processes your speech commands in real time.

🧠 AI-Powered Conversations – Uses Google Gemini API to respond intelligently and naturally to your questions.

🌐 Web Control – Opens popular websites like YouTube, Google, WhatsApp, or LinkedIn with a single voice command.

🎵 Music Search – Finds and plays songs directly on YouTube using yt-dlp.

⏰ Utilities – Tells you the current time, date, weather, and news.

💬 Chat History – Saves your conversations locally in a text file.

🔊 Text-to-Speech – Replies using lifelike AI voice (powered by gTTS).

⚡ Lightweight & Fast – Runs smoothly on Windows using free APIs.

🧩 Tech Stack

Language: Python

AI Model: Google Gemini 1.5 Flash

Speech Recognition: SpeechRecognition (Google API)

Text-to-Speech: gTTS

YouTube Integration: yt-dlp

Audio Playback: playsound

Web Control: webbrowser

🗂 Project Structure
Jarvis/
├── main.py                # Main assistant logic
├── config.py              # Stores Gemini API key
├── chat_history.txt       # Logs past interactions

⚙️ Setup Instructions

Clone the repository:

git clone https://github.com/<your-username>/Jarvis.git
cd Jarvis


Install dependencies:

pip install -r requirements.txt


Add your Gemini API key in config.py:

gemini_api_key = "YOUR_API_KEY_HERE"


Run the assistant:

python main.py

🧠 Example Commands

“Jarvis, open YouTube.”

“Jarvis, play Shape of You.”

“Jarvis, what’s the time?”

“Jarvis, tell me a joke.”

“Jarvis, clear chat history.”

💡 Future Improvements

Add natural-sounding voices (Edge-TTS or ElevenLabs)

Integrate real-time weather & news APIs

Add memory and contextual conversation history

Create a simple GUI with an anime-style avatar

🧑‍💻 Author

Brijrajsinh Jadeja
Final-year Computer Engineering Student | Python & AI Enthusiast
