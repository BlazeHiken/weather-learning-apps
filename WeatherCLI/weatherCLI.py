import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

city = input('Enter a city name: ')
api_key = os.getenv("OPENWEATHER_API_KEY")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    with open("weather.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Weather data saved to weather.json")

    temperature = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    city = data["name"]
    country = data["sys"]["country"]

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]
    sunrise_unix = data["sys"]["sunrise"]
    sunset_unix = data["sys"]["sunset"]
    sunrise_time = datetime.fromtimestamp(sunrise_unix).strftime("%I:%M %p").lstrip("0")
    sunset_time = datetime.fromtimestamp(sunset_unix).strftime("%I:%M %p").lstrip("0")

    print(f"\n{city},{country}")
    print("Weather:")
    print(f"Temperature: {temperature}°C")
    print(f"Condition: {condition.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Coordinates: Latitude {lat}, Longitude {lon}")
    print(f"Sunrise: {sunrise_time}")
    print(f"Sunset: {sunset_time}")

else:
    print("Failed to fetch weather data.")