import sqlalchemy

from modules.database.base import BaseModel


class Activity(BaseModel):
    __tablename__ = 'OT_ACTIVITY_T'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    event_type = sqlalchemy.Column(sqlalchemy.String(128))
    event_date = sqlalchemy.Column(sqlalchemy.DateTime(), default=sqlalchemy.sql.func.current_timestamp())
    description = sqlalchemy.Column(sqlalchemy.String(8192))

    def __init__(self, user_id, event_type, description):
        self.user_id = user_id
        self.event_type = event_type
        self.description = str(description)

    def __repr__(self):
        return '<Activity: user_id={} event_type={} event_date={} description={}>'.format(self.user_id, self.event_type, self.event_date, self.description)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'event_date': self.event_date,
            'description': self.description
        }
