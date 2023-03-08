from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models import User
from flask_app.controllers import validate

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/users/create")
@validate(User) # utilizing custom decorator, that calls the validate method on our model, flashes any error messages, and redirects if its invalid
def create_user():
    session["user_id"] = User.create(**request.form) # ** is used to spread out the request.form dictionary into key word arguments
    return redirect(url_for("wall"))

@app.post("/login")
@validate(User)
def login():
    user = User.retrieve_one(email=request.form['login_email'])
    session["user_id"] = user.id
    return redirect(url_for("wall"))

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))