import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# ========== API CONFIG ==========
API_KEY = "c6c66e9f2fa9010aa277019a055cbc26"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
unit_system = "metric"  # "imperial" for °F

# ========== Weather Fetch ==========
def fetch_weather(city):
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units={unit_system}"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            raise Exception(data["message"])

        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_img = Image.open(io.BytesIO(icon_response.content))

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"].title(),
            "icon": icon_img
        }
    except Exception as e:
        messagebox.showerror("Error", f"Could not get weather: {e}")
        return None

# ========== Update Weather ==========
def update_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Needed", "Please enter a city name.")
        return

    weather = fetch_weather(city)
    if weather:
        temp_label.config(text=f"Temperature: {weather['temp']} °{'C' if unit_system == 'metric' else 'F'}")
        desc_label.config(text=f"Condition: {weather['desc']}")
        wind_label.config(text=f"Wind: {weather['wind']} {'m/s' if unit_system == 'metric' else 'mph'}")
        humidity_label.config(text=f"Humidity: {weather['humidity']}%")
        location_label.config(text=f"{weather['city']}, {weather['country']}")

        icon = ImageTk.PhotoImage(weather["icon"].resize((100, 100)))
        icon_label.config(image=icon)
        icon_label.image = icon  # prevent garbage collection

# ========== Toggle Units ==========
def toggle_unit():
    global unit_system
    unit_system = "imperial" if unit_system == "metric" else "metric"
    unit_button.config(text=f"Switch to {'Celsius' if unit_system == 'imperial' else 'Fahrenheit'}")
    update_weather()

# ========== GUI ==========
app = tk.Tk()
app.title("Weather App")
app.geometry("400x500")
app.config(bg="#f0f8ff")

tk.Label(app, text="Weather Checker", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

city_entry = tk.Entry(app, font=("Arial", 14), justify='center')
city_entry.pack(pady=10)
city_entry.insert(0, "Delhi")

tk.Button(app, text="Get Weather", command=update_weather).pack(pady=5)

unit_button = tk.Button(app, text="Switch to Fahrenheit", command=toggle_unit)
unit_button.pack(pady=5)

location_label = tk.Label(app, font=("Arial", 14), bg="#f0f8ff")
location_label.pack(pady=10)

icon_label = tk.Label(app, bg="#f0f8ff")
icon_label.pack()

temp_label = tk.Label(app, font=("Arial", 14), bg="#f0f8ff")
temp_label.pack()

desc_label = tk.Label(app, font=("Arial", 14), bg="#f0f8ff")
desc_label.pack()

wind_label = tk.Label(app, font=("Arial", 14), bg="#f0f8ff")
wind_label.pack()

humidity_label = tk.Label(app, font=("Arial", 14), bg="#f0f8ff")
humidity_label.pack()

app.mainloop()
