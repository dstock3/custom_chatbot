import requests
from system import config

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?zip=$" + str(config.ZIP) + ",us"

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather():
    response = requests.get(BASE_URL)
    print(response)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = kelvin_to_celsius(data["main"]["temp"])
        temp_min = kelvin_to_celsius(data["main"]["temp_min"])
        temp_max = kelvin_to_celsius(data["main"]["temp_max"])
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_summary = f"{weather_desc}. Temperature: {temp:.1f}°C (min: {temp_min:.1f}°C, max: {temp_max:.1f}°C), Humidity: {humidity}%, Wind speed: {wind_speed} m/s."
        print(weather_summary)
        return weather_summary
    else:
        return f"Error: Unable to fetch weather data for {str(config.ZIP)}."
