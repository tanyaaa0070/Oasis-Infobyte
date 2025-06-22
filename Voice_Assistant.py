import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pywhatkit
import smtplib
import requests
import pyjokes

# ========== Setup ==========
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Weather API key
WEATHER_API_KEY = "c6c66e9f2fa9010aa277019a055cbc26"

# ========== Speak ==========
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== Listen ==========
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t understand.")
        return ""
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting.")
        return ""

# ========== Send Email ==========
def send_email(to_email, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_app_password")
        body = f"Subject: {subject}\n\n{message}"
        server.sendmail("your_email@gmail.com", to_email, body)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print(e)

# ========== Weather ==========
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url).json()
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}.")
    except:
        speak("Could not fetch weather data.")

# ========== Respond to Commands ==========
def run_assistant():
    speak("Hi, I'm your assistant. How can I help?")
    while True:
        command = listen()

        if "stop" in command or "exit" in command:
            speak("Goodbye!")
            break
        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")
        elif "date" in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today is {today}")
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "")
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        elif "open" in command:
            if "youtube" in command:
                webbrowser.open("https://youtube.com")
            elif "google" in command:
                webbrowser.open("https://google.com")
            else:
                speak("Tell me which website to open.")
        elif "play" in command:
            song = command.replace("play", "")
            pywhatkit.playonyt(song)
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            if city:
                get_weather(city)
        elif "joke" in command:
            speak(pyjokes.get_joke())
        elif "email" in command:
            speak("Who is the recipient?")
            to = input("Enter email: ")
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            message = listen()
            send_email(to, subject, message)
        elif "remind me" in command:
            speak("What should I remind you about?")
            reminder = listen()
            speak("Reminder noted.")
            with open("reminder.txt", "a") as f:
                f.write(reminder + "\n")
        elif "read reminders" in command:
            try:
                with open("reminder.txt", "r") as f:
                    reminders = f.readlines()
                    speak("Your reminders are:")
                    for r in reminders:
                        speak(r.strip())
            except:
                speak("No reminders found.")
        else:
            speak("Searching Google...")
            pywhatkit.search(command)

# ========== Start Assistant ==========
run_assistant()
