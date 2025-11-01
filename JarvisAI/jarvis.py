import speech_recognition as sr
import os
import webbrowser
import datetime
from config import gemini_api_key
import google.generativeai as genai
from yt_dlp import YoutubeDL
import os
import tempfile
import threading
from gtts import gTTS
from playsound import playsound


# ========== SETTINGS ==========
WAKE_WORD = "jarvis"
CHAT_HISTORY_FILE = "chat_history.txt"
# TTS_RATE = 200
# TTS_VOLUME = 0.9

chatStr = ""

def say(text):
    print(f"🤖 Jarvis: {text}")
    try:
        threading.Thread(target=play_speech, args=(text,), daemon=True).start()
    except Exception as e:
        print(f"TTS error: {e}")

def play_speech(text):
    try:
        tts = gTTS(text=text, lang='en-au')
        # Create a temporary file path 
        tmp_file = os.path.join(tempfile.gettempdir(), "jarvis_speech.mp3")
        tts.save(tmp_file)
        playsound(tmp_file)
        os.remove(tmp_file)  # Delete after playback
    except Exception as e:
        print(f"Error playing speech: {e}")


# Save chat to file
def save_chat(user, jarvis):
    try:
        with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"User: {user}\nJarvis: {jarvis}\n\n")
    except Exception as e:
        print(f"Chat save error: {e}")

# Gemini Chat
def chat_with_gemini(query):
    try:
        if not gemini_api_key:
            return "Gemini API key missing. Please add it to config.py."

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")  # free and fast
        response = model.generate_content(query)

        if response and response.text:
            return response.text.strip()
        else:
            return "I couldn't find an answer to that, sir."
    except Exception as e:
        return f"Error with Gemini: {str(e)}"
    
#extract video ulr
def get_first_youtube_url(song_name):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extract_flat': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Search and get info dict
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return f"https://www.youtube.com/watch?v={video['id']}"
        except Exception as e:
            print(f"YT-DLP error: {e}")
    return None


# Command handling
def process_command(command):
    global chatStr

    # Normalize
    command = command.lower().strip()

    # --- Websites ---
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "spotify": "https://open.spotify.com",
        "wikipedia": "https://www.wikipedia.com",
        "whatsapp": "https://web.whatsapp.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com"
    }
    for name, url in sites.items():
        if f"open {name}" in command or f"go to {name}" in command or name in command.split():
            webbrowser.open(url)
            say(f"Opening {name} sir")
            return

    # --- Music ---
    if "play" in command:
        song_name = command.split("play", 1)[-1].strip()
        if song_name:
            video_url = get_first_youtube_url(song_name)
            if video_url:
                webbrowser.open(video_url)
                say(f"Playing {song_name} on YouTube sir")
            else:
                say(f"Sorry sir, I couldn't find {song_name}")
        else:
            webbrowser.open("https://open.spotify.com")
            say("Opening Spotify sir")
        return

    # --- Time ---
    if "time" in command:
        now = datetime.datetime.now()
        hour = now.strftime("%I").lstrip("0") or "12"
        minute = now.strftime("%M")
        period = now.strftime("%p")
        say(f"Sir, the time is {hour}:{minute} {period}")
        return

    # --- Date ---
    if "date" in command or "today" in command:
        today = datetime.date.today()
        say(f"Sir, today is {today.strftime('%A, %B %d, %Y')}")
        return

    # --- Weather ---
    if "weather" in command:
        webbrowser.open("https://weather.com")
        say("Opening weather website sir")
        return

    # --- News ---
    if "news" in command:
        webbrowser.open("https://news.google.com")
        say("Opening news sir")
        return

    # --- Reset Chat ---
    if "reset chat" in command:
        chatStr = ""
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
        say("Chat history cleared sir")
        return

    # --- Exit ---
    if any(word in command for word in ["quit", "exit", "goodbye", "stop"]):
        say("Goodbye sir. Have a great day.")
        os._exit(0)

    # --- AI Chat ---
    ai_reply = ai_reply = chat_with_gemini(command)
    say(ai_reply)
    chatStr += f"User: {command}\nJarvis: {ai_reply}\n"
    save_chat(command, ai_reply)

# Background listening
def callback(recognizer, audio):
    try:
        query = recognizer.recognize_google(audio, language="en-in").lower()
        print(f"🗣 Heard: {query}")
        if WAKE_WORD in query:
            command = query.split(WAKE_WORD, 1)[-1].strip()
            if command:
                process_command(command)
            else:
                say("Yes sir?")
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")

def main():
    say("Jarvis online and listening for your command sir.")
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)

    r.listen_in_background(mic, callback)

    # Keep program running
    while True:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("Goodbye sir")
    except Exception as e:
        print(f"Error: {e}")
