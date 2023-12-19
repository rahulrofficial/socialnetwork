""" models.py file"""
 
# SQLAlchemy Instance Is Imported
from app import db
 
# Declaring Model
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name=db.Column(db.String(80), nullable=True)
    last_name=db.Column(db.String(80), nullable=True)
    profile_pic_addr=db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    
class Posts(db.Model):
    __tablename__ = "posts"
 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

class UserPosts(db.Model):
    __tablename__ = "user_posts"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)
    
class Followers(db.Model):
    __tablename__ = "followers"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)