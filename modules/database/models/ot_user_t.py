import sqlalchemy
from passlib.apps import custom_app_context as pwd_context

import modules.database.base as base


class User(base.BaseModel):
    __tablename__ = 'OT_USER_T'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(100))
    password = sqlalchemy.Column(sqlalchemy.String(20))
    email = sqlalchemy.Column(sqlalchemy.String(50))
    active = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, username, password, email, active=1):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.email = email
        self.active = active

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
        }

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
