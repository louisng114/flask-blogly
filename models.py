from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Models for Blogly."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    image_url = db.Column(db.String, nullable=False, default="https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg")

    def get_full_name(self):
        """return full name of user"""
        return self.first_name + self.last_name if self.last_name is not None else self.first_name
