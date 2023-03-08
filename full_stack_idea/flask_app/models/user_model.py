from flask_app import bcrypt
from . import base_model, message_model
from dataclasses import dataclass
from datetime import datetime # importing datetime so we can use it as a type annotation in our class
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Utilizing data classes allows us to write our models in a cleaner way
# now we no longer need to manually assign data to the objects, we can simply pass key word arguments into the constructor
# dataclasses also automatically define some helper dunder methods such as __eq__ which allows us to compare two different objects
@dataclass
class User(base_model.Model): # inherit our base class
    id : int # we have to provide the type annotations when using data classes
    username : str
    email : str
    password : str
    created_at : datetime
    updated_at : datetime
    table : str = "users" # this is the table name in our database, it has to match exactly since it is used to generate our queries
    # the property decorator allows us to have functions as properties that are evaluated upon access
    # this is nice because it only retrieves the associated data when it is actually needed, rather than getting it for every single object
    @property
    def received_messages(self):
        # notice even though this is a retrieve_all we can still pass in data to be used in the where clause due to how we structured our base model
        # we can pass our data in as key word arguments due to using the ** operator in the base model
        return message_model.Message.retrieve_all(receiver_id=self.id)
    
    @property
    def sent_messages(self):
        return message_model.Message.retrieve_all(sender_id=self.id)
    
    @classmethod
    def create(cls, **data):
        data['password'] = bcrypt.generate_password_hash(data['password']) # hash the password
        data.pop("confirm_password") # remove the confirm password
        return super().create(**data)
    
    @staticmethod
    def validate(**data): # TODO clean up and refactor
        errors = {}
        user = User.retrieve_one(email = data['email'] if 'email' in data else data['login_email'])

        # creation validations
        if "username" in data and len(data["username"]) < 2:
            errors["username"] = "Username should be at least 2 characters"
        if "email" in data and not EMAIL_REGEX.match(data['email']):
            errors["email"] = "Email format is invalid"
        elif "email" in data and user:
            errors['email'] = "Email is already in use"
        if 'password' in data and len(data['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        elif 'confirm_password' in data and 'password' in data and data['password'] != data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'

        # login validations
        if "login_email" in data and not (user and bcrypt.check_password_hash(user.password, data['login_password'])):
            errors['login'] = 'Invalid Credentials'

        return errors