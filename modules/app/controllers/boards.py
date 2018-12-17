import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database import Board, add_board
from modules.database.crud import crud_board

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/boards', methods=['GET'])
@auth_required
def boards(user_id):
    status_code = 200
    data = crud_board.find_boards_by_user_id(user_id)
    if data is None:
        status_code = 404
        data = {'status': 'failed', 'message': 'Not found user', 'resource_id': user_id}
    return make_response(jsonify(data), status_code)


@app.route('/board', methods=['POST'])
@auth_required
def add_new_board(user_id):
    payload = request.get_json()
    o = Board.deserialize(payload)
    o.user_id = user_id
    status_code, board_id = add_board(o)
    data = {'status': 'success', 'message': 'Created new board', 'resource_id': board_id}
    return make_response(jsonify(data), status_code)
