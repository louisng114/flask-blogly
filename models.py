from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model for Blogly."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    image_url = db.Column(db.String, nullable=False, default="https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg")

    def get_full_name(self):
        """return full name of user"""
        return self.first_name + " " + self.last_name if self.last_name is not None else self.first_name

class Post(db.Model):
    """Post model for Blogly."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String, nullable=False, default=datetime.now())
    user = db.Column(db.Integer, db.ForeignKey("users.id"))

    poster = db.relationship("User", backref="posts")

    tags = db.relationship("Tag", secondary="posttags", backref="posts")

class Tag(db.Model):
    """Tag model for Blogly"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)
    name = db.Column(db.String, unique=True)

class PostTag(db.Model):
    """Through for Post and Tag"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
