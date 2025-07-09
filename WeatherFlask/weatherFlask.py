from flask import Flask, render_template, request
import requests, json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
@app.route("/", methods=["GET"])
def index():
    city = request.args.get("city")
    weather = None
    error = None
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if city:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open("weather.json", "w") as file:
                json.dump(data, file, indent=4)
            print("Weather data saved to weather.json")

            weather = {
                "temperature" : data["main"]["temp"],
                "condition" : data["weather"][0]["description"],
                "humidity" : data["main"]["humidity"],
                "wind_speed" : data["wind"]["speed"],
                "city" : data["name"],
                "country" : data["sys"]["country"],
                "lat" : data["coord"]["lat"],
                "lon" : data["coord"]["lon"],
                "sunrise_time" : datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p").lstrip("0"),
                "sunset_time" : datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p").lstrip("0")
            }

        else:
            error = f"City '{city}' not found."
    
    return render_template("index.html", weather=weather, error=error if city else None)
    
    
if __name__ == "__main__":
    app.run(debug=True)