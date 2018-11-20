import os
from flask import request, jsonify, make_response
from modules.app import app
from modules import logger
from modules.database.finders import board_finder

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/<username>/boards', methods=['GET', 'POST'])
def boards(username):
    if request.method == 'GET':
        query = request.args
        data = board_finder.find_boards_by_username(username)
        return make_response(jsonify(data), 200)
