from sqlalchemy import Column, String, Integer
from modules.database.base import BaseModel

class List(BaseModel):
    __tablename__ = 'OT_LIST_T'

    id = Column(Integer, primary_key=True)
    board_id = Column(Integer)
    name = Column(String(200))


    def __init__(self, name, board_id):
        self.name = name
        self.board_id = board_id
