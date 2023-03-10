from flask import request, redirect, flash, session, url_for
from functools import wraps

# Define our helper decorators
def validate_model(cls): # usage: @validate(User) above a controller method
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # call the models validate method and pass in data from request.form as key word arguments
            errors = cls.validate(**request.form)
            if errors:
                # if the errors dictionary isn't empty, we want to iterate over it and flash all of the errors
                for category, message in errors.items():
                    flash(message,category)
                # then we want to redirect back to where we came from
                return redirect(request.referrer)
            return func(*args, **kwargs)
        return wrapper
    return inner

def enforce_login(func): # usage: @enforce_login above a controller method
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that user_id is in session and redirect to index if it's not
        if "user_id" not in session:
            return redirect(url_for("index"))
        return func(*args,**kwargs)
    return wrapper