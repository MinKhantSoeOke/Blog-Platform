from datetime import datetime
from app import db, login_manager, bcrypt
from flask_login import UserMixin
from passlib.pwd import genword

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model to represent users in the database
class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    password    = db.Column(db.String(60), nullable=False)
    posts       = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    @staticmethod
    def generate_random_password(length=12):
        password = genword(length=length)
        return password
    
# Post model to represent blog posts in the database
class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content     = db.Column(db.Text, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments    = db.relationship('Comment', backref='post', lazy=True)
    likes       = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    @property
    def like_count(self):
        return len(self.likes)
    
    @property
    def comment_count(self):
        return len(self.comments)
    
# Comment model to represent comments on posts in the database
class Comment(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    content     = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_name   = db.Column(db.String(20), nullable=False)
    post_id     = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

# Like model to represent likes on posts in the database
class Like(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id     = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.user_id}', '{self.post_id}')"
