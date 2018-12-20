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

    def __repr__(self):
        return 'List name={} board_id={}>'.format(self.name, self.board_id)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'board_id' : self.board_id,
        }

    @staticmethod
    def deserialize(json_obj):
        if not isinstance(json_obj, dict):
            raise Exception('Deserialize exception')
        try:
            board_id = json_obj['board_id']
            name = json_obj['name']
            li = List(name, board_id)
            return li
        except Exception:
            raise Exception('Deserialize exception')
