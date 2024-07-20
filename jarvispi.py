import openai
import speech_recognition as sr
import pyttsx3
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init(driverName='espeak')
tts_engine.setProperty('rate', 150)  # Set speaking rate
tts_engine.setProperty('volume', 1.0)  # Set volume level (0.0 to 1.0)

def listen_for_wake_word(wake_word="jarvis"):
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if wake_word in text:
                    print(f"Wake word '{wake_word}' detected.")
                    return
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def record_audio():
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Command received: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def get_gpt4o_mini_response(prompt):
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    while True:
        listen_for_wake_word()
        command = record_audio()
        if command:
            response = get_gpt4o_mini_response(command)
            print(f"GPT-4o-mini Response: {response}")
            speak_text(response)
        time.sleep(1)  # Small delay to avoid high CPU usage

if __name__ == "__main__":
    main()
