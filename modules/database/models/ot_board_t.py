from sqlalchemy import Column, String, Integer

from modules.database.base import BaseModel


class Board(BaseModel):
    __tablename__ = 'OT_BOARD_T'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    bg_color = Column(String(10))
    active = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, name, bg_color, active):
        self.name = name
        self.bg_color = bg_color
        self.active = active

    def __repr__(self):
        return '<Board: name={} bg_color={}>'.format(self.name, self.bg_color)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'bg_color': self.bg_color,
        }
