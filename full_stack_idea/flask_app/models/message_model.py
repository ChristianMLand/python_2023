from . import base_model, user_model
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message(base_model.Model):
    id : int
    content : str
    created_at : datetime
    updated_at : datetime
    sender_id : int
    receiver_id : int
    table : str = "messages"

    @property
    def receiver(self):
        return user_model.User.retrieve_one(id=self.receiver_id)

    @property
    def sender(self):
        return user_model.User.retrieve_one(id=self.sender_id)

    @staticmethod
    def validate(**data):
        errors = {}
        if "content" in data and len(data["content"]) < 5:
            errors["content"] = "Content should be at least 5 characters long"
        return errors
