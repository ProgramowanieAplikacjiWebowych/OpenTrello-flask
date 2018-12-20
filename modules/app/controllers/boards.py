import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database import Board, add_board, update_board
from modules.database.crud import crud_board
from modules.database.crud.crud_activity import add_activity
from modules.database.models.ot_activity_t import Activity

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/boards', methods=['GET'])
@auth_required
def get_boards(user_id):
    status_code = 200
    data = crud_board.find_boards_by_user_id(user_id)
    if data is None:
        status_code = 404
        data = {'status': 'failed', 'message': 'Not found user', 'resource_id': user_id}
    LOG.debug(data)
    return make_response(jsonify(data), status_code)


@app.route('/<id>/board', methods=['GET'])
@auth_required
def get_board_with_data(user_id, id):
    status_code = 200
    data = crud_board.find_board_with_related_data_by_board_id(id)
    LOG.debug(data)
    return make_response(data.to_json(), status_code)


@app.route('/board', methods=['POST'])
@auth_required
def create_board(user_id):
    payload = request.get_json()
    board = Board.deserialize(payload)
    board.user_id = user_id
    status_code, board_id = add_board(board)
    data = {'status': 'success', 'message': 'Created new board', 'resource_id': board_id}
    LOG.debug(board)
    activity = Activity(user_id, "CREATE_BOARD", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<id>/board', methods=['PUT'])
@auth_required
def modify_board(user_id, id):
    payload = request.get_json()
    board = Board.deserialize(payload)
    board.id = id
    board.user_id = user_id
    status_code, board_id = update_board(board)
    data = {'status': 'success', 'message': 'Updated board', 'resource_id': board_id}
    LOG.debug(board)
    activity = Activity(user_id, "MODIFY_BOARD", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)
