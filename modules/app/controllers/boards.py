import os
from flask import request, jsonify, make_response
from modules.app import app
from modules import logger
from modules.database import find_user_by_username, Board
from modules.database.finders import board_finder
from modules.database.services.board_repository import add_board

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/<username>/boards', methods=['GET'])
def boards(username):
    status_code = 200
    data = board_finder.find_boards_by_username(username)
    if data is None:
        status_code = 404
        data = {'message':'not found', 'resource':username}
    return make_response(jsonify(data), status_code)


@app.route('/<username>/board', methods=['POST'])
def add_new_board(username):
    payload = request.json
    user = find_user_by_username(username)
    status_code = 404
    data = {'message':'not found', 'resource':username}
    if user is not None:
        o = Board.deserialize(payload)
        o.user_id = user.id
        status_code, resource_id = add_board(o)
        data = {'message':'created', 'resource_id':resource_id}
    return make_response(jsonify(data), status_code)
