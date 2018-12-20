from sqlalchemy import Column, String, Integer

from modules.database.base import BaseModel


class Board(BaseModel):
    __tablename__ = 'OT_BOARD_T'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    bg_color = Column(String(10))
    active = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, name, bg_color='', active=1):
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
            'active': self.active
        }

    @staticmethod
    def deserialize(json_obj):
        if not isinstance(json_obj, dict):
            raise Exception('Deserialize exception')
        try:
            name = json_obj['name']
            board = Board(name)
        except Exception:
            raise Exception('Deserialize exception')

        if 'bg_color' in json_obj:
            board.bg_color = json_obj['bg_color']
        if 'active' in json_obj:
            board.active = json_obj['active']
        return board
