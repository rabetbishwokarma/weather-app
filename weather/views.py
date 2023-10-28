from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from datetime import datetime as dt

def home(request):
    load_dotenv()
    user_api = os.getenv('API_KEY')
    
    if request.method == 'POST':
        location = request.POST.get('city', '') 
    else:
        location = '' 

    if not location:
        error_message = "Please enter a city name."
        return render(request, 'home.html', {'error_message': error_message})

    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if api_data.get('cod') == 404:
        error_message = "Invalid City: Please check your city name."
        return render(request, 'home.html', {'error_message': error_message})
    
    temp_city = round(api_data['main']['temp'] - 273.15, 2)  # Convering temperature to Celsius and round to 2 decimal places
    weather_description = api_data['weather'][0]['description']
    humidity = api_data['main']['humidity']
    wind_speed = api_data['wind']['speed']
    date_time = ('Here is the Weather Stats')
    

    weather_info = {
        "location": location,
        "date_time": date_time,
        "temperature": temp_city,
        "weather_description": weather_description,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "weather_stat": ("Here is the Weather Stats for:")
    }

    icon_name = map_weather_to_icon(weather_description)
    return render(request, 'home.html', {'weather_info': weather_info, 'weather_icon': icon_name})

def map_weather_to_icon(weather_description):
    icons = {
        "clear": "sunny.png",
        "cloud": "sunny.png",
        "rain": "sunny.png",
    }
    # Default icon
    default_icon = "sunny.png"
    return f"weather/media/{icons.get(weather_description, default_icon)}"
