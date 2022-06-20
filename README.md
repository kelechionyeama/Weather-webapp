# Discover.IO by Kelechi Onyeama
### Video Demo: https://youtu.be/7Sdh8OgCsO4
### Description: Weather web application

# Functionalities
This is a simple web application for checking the weather in any city worldwide.
Discover.IO allows users to register, login and create an account. Users can click on the weather icon and type in any city or country worldwide to get a thorough description of the current weather state in the said location.
API provided by OpenWeather.org


# App.py
App.py contains the back end of the application.

I imported a bunch of libaries to use with my application.

I used sessions to keep users logged in and also used werkzeug.security to hash users passwords to make in harder to guess when storing in the database.

CS50 SQL was used as the local database

# Helpers.py
Helpers file was imported into app.py.

This file contains the configurations for the API used from OpenWeather.org.

Openweather.org did'nt have all the information I needed in one API so I nested 2 of their APIs together. I got data from one and used it into another API to get all required information.

# Templates
This folder contains all the html pages for this website.

Jinja was used to make it easier.

# Static
Contains css and bootstrap used for implemtation and design