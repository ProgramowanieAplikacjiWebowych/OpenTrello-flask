import os
from flask import request, jsonify
from modules.app import app
from modules import logger
from modules.database import finders

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/<username>/boards', methods=['GET', 'POST'])
def boards(username):
    if request.method == 'GET':
        query = request.args
        data = finders.find_all_boards()
        return jsonify(data), 200

    # data = request.get_json()
    # if request.method == 'POST':
    #     if data.get('name', None) is not None and data.get('bg_color', None) is not None:
    #         mongo.db.users.insert_one(data)
    #         return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400