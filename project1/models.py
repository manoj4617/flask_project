from project1 import db 
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))


class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userid = db.Column(db.Integer , db.ForeignKey("user.id") , nullable = False)
    title = db.Column(db.String(50) , default = 'My post')
    post = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    regdate = db.Column(db.DateTime ,nullable = False )

class LikedPosts(UserMixin, db.Model):
    __tablename__ = "liked_post"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
