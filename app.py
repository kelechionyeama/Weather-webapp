import os

from cs50 import SQL
from flask import Flask, render_template, redirect, request, flash, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_city, get_weather, login_required

#Configure application
app = Flask(__name__)

#Configure CS50 Libary to use SQL
"""LEARN OTHER TYPES OF SQL"""

db = SQL("sqlite:///discover.db")

#Configure session to use filesystem instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Ensure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Ensure Api Key has been set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():

    if request.method == "POST":

        if not request.form.get("city"):
            return render_template("flashed.html", header_text="Failed", text="Must provide a City")

        city = get_city(request.form.get("city"))

        Lat = city["lat"]
        Lon = city["lon"]

        weathers = get_weather(Lat, Lon)

        return render_template("weathers.html", weathers=weathers, location=request.form.get("city").upper())

    return render_template("weather.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("flashed.html", header_text="Failed", text="Must provide a username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("flashed.html", header_text="Failed", text="Must provide a password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return  render_template("flashed.html", header_text="Failed", text="Invalid username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("home.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        #Ensure parameters
        if not request.form.get("username"):
            return render_template("flashed.html", header_text="Failed", text="Must input username!!")

        elif not request.form.get("password"):
            return render_template("flashed.html", header_text="Failed", text="Must input password!!")

        elif not request.form.get("Cpassword"):
            return render_template("flashed.html", header_text="Failed", text="Must input password!!")

        elif request.form.get("password") != request.form.get("Cpassword"):
            return render_template("flashed.html", header_text="Failed", text="Password does not match!!")

        #Insert into database
        try:
            db.execute("INSERT INTO users (username, password) VALUES(?,?)", request.form.get("username"),
             generate_password_hash(request.form.get("password"), "pbkdf2:sha256", len(request.form.get("password"))))

        except:
            return render_template("flashed.html", header_text="Failed", text="Username has been taken")

        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():

    #Clear session and log user out
    session.clear()

    return redirect("/")

