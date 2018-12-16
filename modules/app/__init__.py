import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask
from flask_jwt_extended import JWTManager

from modules.database.base import BaseModel


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        if isinstance(o, BaseModel):
            return o.serialize()
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)
app.json_encoder = JSONEncoder


from modules.app.controllers import *