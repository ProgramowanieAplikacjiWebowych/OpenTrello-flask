import sqlalchemy

from modules.database.base import BaseModel


class Comment(BaseModel):
    __tablename__ = 'OT_COMMENT_T'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    object_type = sqlalchemy.Column(sqlalchemy.String(15))
    object_id = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.String(8192))

    def __init__(self, description, user_id=None, object_type=None, object_id=None):
        self.user_id = user_id
        self.object_type = object_type
        self.object_id = object_id
        self.description = description

    def __repr__(self):
        return '<Card: user_id={} object_type={} object_id={} description={}>'.format(self.user_id, self.object_type, self.object_id, self.description)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'object_type': self.object_type,
            'object_id': self.object_id,
            'description': self.description
        }

    @staticmethod
    def deserialize(json_obj):
        if not isinstance(json_obj, dict):
            raise Exception('Deserialize exception')
        try:
            description = json_obj['description']
            comment = Comment(description)
        except Exception:
            raise Exception('Deserialize exception')

        if 'user_id' in json_obj:
            comment.user_id = json_obj['user_id']
        if 'object_type' in json_obj:
            comment.object_type = json_obj['object_type']
        if 'object_id' in json_obj:
            comment.object_id = json_obj['object_id']
        return comment
