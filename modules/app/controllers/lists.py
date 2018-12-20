import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database import List, add_list, update_list
from modules.database.crud.crud_activity import add_activity
from modules.database.models.ot_activity_t import Activity

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/list', methods=['POST'])
@auth_required
def create_list(user_id):
    payload = request.get_json()
    li = List.deserialize(payload)
    status_code, list_id = add_list(li)
    data = {'status': 'success', 'message': 'Created new list', 'resource_id': list_id}
    LOG.debug(li)
    activity = Activity(user_id, "CREATE_LIST", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<id>/list', methods=['PUT'])
@auth_required
def modify_list(user_id, id):
    payload = request.get_json()
    li = List.deserialize(payload)
    li.id = id
    status_code, list_id = update_list(li)
    data = {'status': 'success', 'message': 'Updated list', 'resource_id': list_id}
    LOG.debug(li)
    activity = Activity(user_id, "MODIFY_LIST", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)
