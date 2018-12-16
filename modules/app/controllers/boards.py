import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database import find_user_by_username, Board, add_board
from modules.database.crud import crud_board

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/<username>/boards', methods=['GET'])
@auth_required
def boards(username):
    status_code = 200
    data = crud_board.find_boards_by_username(username)
    if data is None:
        status_code = 404
        data = {'status': 'failed', 'message': 'Not found {username}'}
    return make_response(jsonify(data), status_code)


@app.route('/<username>/board', methods=['POST'])
@auth_required
def add_new_board(username):
    payload = request.json
    user = find_user_by_username(username)
    status_code = 404
    data = {'status': 'success', 'message': 'not found {username}'}
    if user is not None:
        o = Board.deserialize(payload)
        o.user_id = user.id
        status_code, resource_id = add_board(o)
        data = {'status': 'success', 'message': 'created resource_id {resource_id}'}
    return make_response(jsonify(data), status_code)
