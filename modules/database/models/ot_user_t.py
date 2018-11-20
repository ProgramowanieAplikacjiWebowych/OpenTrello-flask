from sqlalchemy import Column, String, Integer, ForeignKey

from modules.database.base import BaseModel


class User(BaseModel):
    __tablename__ = 'OT_USER_T'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(20))
    email = Column(String(50))
    active = Column(Integer)

    def __init__(self, username, password, email, active):
        self.username = username
        self.password = password
        self.email = email
        self.active = active

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
        }
