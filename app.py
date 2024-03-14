"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home_redirect():
    return redirect ("/users")

@app.route("/users")
def users_page():
    users = User.query.all()
    return render_template("listing.html", users=users)

@app.route("/users/new")
def new_user_page():
    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def new_user_form_handle():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    if image_url == "":
        image_url = None
    
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details_page(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def user_edit_page(user_id):
    return render_template("user_edit.html", user_id=user_id)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_edit_handle(user_id):
    form_data = request.form
    new_first_name = form_data.get("first_name")
    new_last_name = form_data.get("last_name")
    new_image_url = form_data.get("image_url")

    user = User.query.get_or_404(user_id)
    if new_first_name != "":
        user.first_name = new_first_name
    if new_last_name != "":
        user.last_name = new_last_name
    if new_image_url != "":
        user.image_url = new_image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete_handle(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")
