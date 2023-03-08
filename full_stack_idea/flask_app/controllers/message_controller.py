from flask import redirect, render_template, request, session, url_for
from flask_app import app
from flask_app.models import User, Message
from flask_app.controllers import enforce_login, validate

@app.get("/wall")
@enforce_login # custom enforce_login decorator simple checks if a user_id is in session, and redirects them to the login page if not
def wall():
    context = {
        "logged_user" : User.retrieve_one(id=session["user_id"]),
        "all_users" : User.retrieve_all()
    }
    # utilizing this context dictionary that we spread out into key word arguments just makes our code a bit more readable and consistent
    return render_template("wall.html", **context)

@app.post("/messages/create")
@enforce_login
@validate(Message) # once again using our validate decorator, but this time passing in the Message model
def create_message():
    Message.create(sender_id=session["user_id"], **request.form)
    return redirect(url_for('wall'))

@app.get("/messages/delete/<int:id>")
@enforce_login
def delete_message(id):
    message = Message.retrieve_one(id=id)
    # make sure that the person is actually allowed to delete the message before doing so
    if message.receiver_id == session["user_id"]:
        Message.delete(id=id)
    return redirect(url_for('wall'))

