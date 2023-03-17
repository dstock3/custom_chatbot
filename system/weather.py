import requests
from system import config

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?zip=" + str(config.ZIP) + ",us&units=imperial&appid=" + config.OPENWEATHERMAP_API_KEY

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather():
    response = requests.get(BASE_URL)
   
    if response.status_code == 200:
        data = response.json()
        forecasts = data['list']
        formatted_forecasts = []

    if response.status_code == 200:
        data = response.json()
        forecasts = data['list']
        formatted_forecasts = []

        for forecast in forecasts:
            date = forecast['dt_txt']
            temperature = forecast['main']['temp']
            weather_description = forecast['weather'][0]['description']
            wind_speed = forecast['wind']['speed']

            formatted_forecast = {
                "date": date,
                "temperature": temperature,
                "weather_description": weather_description,
                "wind_speed": wind_speed
            }
            formatted_forecasts.append(formatted_forecast)

        return {"location": str(config.ZIP), "forecasts": formatted_forecasts}

    else:
        return {"error": f"Unable to fetch weather data for {str(config.ZIP)}. Error code: {response.status_code}"}
