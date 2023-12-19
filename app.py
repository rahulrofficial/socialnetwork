import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configure CS50 Library to use SQLite database
db = SQL("sqlite:///starnetwork.db")


@app.after_request
def after_request(response):
   
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password", 403)

        # Query database for username
        
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
    
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return ("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    users = db.execute("SELECT username FROM users;")
    usernames = [user["username"] for user in users]

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        print(email)
        if not username:
            return  ("must provide username", 400)
        elif username in usernames:
            return  ("username already exists", 400)
        elif not email:
            return  ("must provide email", 400)

        # Ensure password was submitted
        elif not password:
            return  ("must provide password", 400)
        elif not confirmation:
            return  ("must confirm password", 400)
        elif not password == confirmation:
            return  ("Passwords does not match", 400)

        hashed_pass = generate_password_hash(password)
        success = db.execute(
            "INSERT INTO users (username,hash,email) VALUES (?,?,?)", username, hashed_pass,email
        )
        if success:
            return redirect("/login")
        else:
            return  ("Registration Failed", 403)

    return render_template("register.html")