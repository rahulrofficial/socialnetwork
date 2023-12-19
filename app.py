import os


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

basedir=os.path.abspath(os.path.dirname(__file__))
# Configuring SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///"+os.path.join(basedir,"starnetwork.db")

# Suppresses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialising SQLAlchemy with Flask App
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import Users,Posts

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
            return render_template("login.html",message="must provide username")
            

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",message="must provide password")
            

        # Query database for username
        print(request.form.get("username"))
        rows = Users.query.filter_by(username=request.form.get("username")).all()
        print("rows",rows[0].hash)
    
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0].hash, request.form.get("password")
        ):
            return render_template("login.html",message="invalid username and/or password")
            

        # Remember which user has logged in
        session["user_id"] = rows[0].id

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
    
    users = Users.query.all()
    usernames = [user.username for user in users]
    
    
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        print(email)
        if not username:
            return render_template("register.html",message="must provide username")
        
        elif username in usernames:
            return render_template("register.html",message="username already exists")
            
        elif not email:
            return render_template("register.html",message="must provide email")            
            

        # Ensure password was submitted
        elif not password:
            return render_template("register.html",message="must provide password")
            
        elif not confirmation:
            return render_template("register.html",message="must confirm password")
            
        elif not password == confirmation:
            return render_template("register.html",message="Passwords does not match")            

        hashed_pass = generate_password_hash(password)
        add_user=Users(          
            username=username,
            hash=hashed_pass,
            email=email
        )
        db.session.add(add_user)
        db.session.commit()
        if add_user.id:
            return redirect("/login")
        else:
            return render_template("register.html",message="Registration Failed")
            

    return render_template("register.html")














 

 
if __name__ == "__main__":  
    
    app.run(debug=True)