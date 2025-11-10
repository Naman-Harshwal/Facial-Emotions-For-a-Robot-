import speech_recognition as sr  # ✅ Correct
import pyttsx3
import openai
from dotenv import load_dotenv
import os

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except:
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

# Main loop
while True:
    user_input = listen()
    if "exit" in user_input.lower():
        speak("Goodbye!")
        break
    if user_input:
        response = get_ai_response(user_input)
        print(f"AI: {response}")
        speak(response)