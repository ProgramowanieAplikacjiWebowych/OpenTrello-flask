import sqlalchemy

from modules.database.base import BaseModel


class Card(BaseModel):
    __tablename__ = 'OT_CARD_T'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    list_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String(128))
    date_to = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String(8192))

    def __init__(self, list_id, name, description='', date_to=None):
        self.list_id = list_id
        self.name = name
        self.description = description
        self.date_to = date_to

    def __repr__(self):
        return '<Card: list_id={} name={} date_to={} description={}>'.format(self.list_id, self.name, self.date_to, self.description)

    def serialize(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'name': self.name,
            'description': self.description,
            'date_to': self.date_to,
        }

    @staticmethod
    def deserialize(json_obj):
        if isinstance(json_obj, dict):
            try:
                list_id = json_obj['list_id']
                name = json_obj['name']
                card = Card(list_id, name)
            except Exception:
                raise Exception('Deserialize exception')

            if 'description' in json_obj:
                card.description = json_obj['description']
            if 'date_to' in json_obj:
                card.date_to = json_obj['date_to']
            return card
