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

# Declaring Model
follow = db.Table(
    'follow',
    db.Column('following_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'))
)
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name=db.Column(db.String(80), nullable=True)
    last_name=db.Column(db.String(80), nullable=True)
    profile_pic_addr=db.Column(db.String(200), nullable=True)
    user_posts=db.relationship('Posts',backref='owner',lazy='dynamic')
    followers = db.relationship('Users', 
                                secondary = follow, 
                                primaryjoin = (follow.c.following_id == id),
                                secondaryjoin = (follow.c.follower_id == id),
                                backref = 'following'
                                )
    def __repr__(self):
        return '<User %r>' % self.username
    
    
class Posts(db.Model):
    __tablename__ = "posts"
 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)


    

@app.after_request
def after_request(response):   
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    
    
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("current_post"):
            return render_template("index.html",message="must provide a post")
        print(request.form.get("current_post"))
        post=Posts(
            content=request.form.get("current_post"),
            person_id=session["user_id"]
        )
        db.session.add(post)
        db.session.commit()
        print("Post added")
        redirect("/")
    posts=Posts.query.all()
    return render_template("index.html",posts=posts)


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




@app.route("/test", methods=["GET", "POST"])
def test():
    
    harry =Users.query.filter_by(username='harry').first()
    ron=Users.query.filter_by(username='Ron').first()
    print(ron.following)
    return render_template("test.html")









 

 
if __name__ == "__main__":  
    
    app.run(debug=True)