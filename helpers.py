#API FOR WEATHER APP
import os
import requests
import urllib.parse
from functools import wraps

from flask import redirect, request, session

#Get Api key from user
api_key = os.environ.get("API_KEY")

#Required login function
"""Function decorator """
def login_required(f):
    wraps(f)
    def decorated_function(*args, **kwargs):
        """TODO"""
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


#Get City from user using Geocoding API
def get_city(city):
    """Look up City"""

    #Contact API
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote_plus(city)}&limit=5&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    #Parse/Work with response and get lat and lon
    """Get lat and lon"""

    quote = response.json()[0]
    return {
        "lat": quote["lat"],
        "lon": quote["lon"]
    }

def get_weather(lat, lon):
    """Look up weather info"""

    #Contact API
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={urllib.parse.quote_plus(str(lat))}&lon={urllib.parse.quote_plus(str(lon))}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    #Parse/Work with response and get weather info

    quote = response.json()

    return {
        "lat": quote["coord"]["lat"],
        "lon": quote["coord"]["lon"],
        "description": quote["weather"][0]["description"],
        "temperature": quote["main"]["temp"],
        "feels_like": quote["main"]["feels_like"],
        "wind": quote["wind"]["speed"],
        "country": quote["sys"]["country"],
        "sunrise": quote["sys"]["sunrise"],
        "sunset": quote["sys"]["sunset"]
    }