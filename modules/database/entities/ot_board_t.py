from sqlalchemy import Column, String, Integer
from modules.database.base import Base

class Board(Base):
    __tablename__ = 'OT_BOARD_T'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    bg_color = Column(String(10))
    active = Column(Integer)

    def __init__(self, name, bg_color, active):
        self.name = name
        self.bg_color = bg_color
        self.active = active