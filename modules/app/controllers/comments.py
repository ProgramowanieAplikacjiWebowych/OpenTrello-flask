import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database.crud.crud_activity import add_activity
from modules.database.crud.crud_comment import add_comment, update_comment, delete_comment
from modules.database.models.ot_activity_t import Activity
from modules.database.models.ot_comment_t import Comment

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

OBJECT_TYPES = ['CARD', 'ATTACHMENT']


@app.route('/<object_type>/<object_id>/comment', methods=['POST'])
@auth_required
def create_comment(user_id, object_type, object_id):
    object_type = object_type.upper()
    if object_type not in OBJECT_TYPES:
        status_code = 404
        data = {'status': 'failed', 'message': 'Adding new comment failed, unsupported object type', 'resource_id': object_id}
        return make_response(jsonify(data), status_code)
    payload = request.get_json()
    comment = Comment.deserialize(payload)
    comment.object_id = object_id
    comment.object_type = object_type
    comment.user_id = user_id
    status_code, comment_id = add_comment(comment)
    data = {'status': 'success', 'message': 'Created new comment', 'resource_id': comment_id}
    LOG.debug(comment)
    activity = Activity(user_id, "CREATE_COMMENT", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<object_type>/<object_id>/comment', methods=['PUT'])
@auth_required
def modify_comment(user_id, object_type, object_id):
    object_type = object_type.upper()
    if object_type not in OBJECT_TYPES:
        status_code = 404
        data = {'status': 'failed', 'message': 'Modifying comment failed, unsupported object type', 'resource_id': object_id}
        return make_response(jsonify(data), status_code)
    payload = request.get_json()
    comment = Comment.deserialize(payload)
    comment.object_id = object_id
    comment.object_type = object_type
    comment.user_id = user_id
    status_code, comment_id = update_comment(comment)
    data = {'status': 'success', 'message': 'Created new comment', 'resource_id': comment_id}
    LOG.debug(comment)
    activity = Activity(user_id, "MODIFY_COMMENT", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<object_type>/<object_id>/comment', methods=['DELETE'])
@auth_required
def delete_comment(user_id, object_type, object_id):
    if object_type not in OBJECT_TYPES:
        status_code = 404
        data = {'status': 'failed', 'message': 'Modifying comment failed, unsupported object type', 'resource_id': object_id}
        return make_response(jsonify(data), status_code)
    status_code, comment_id = delete_comment(object_id)
    data = {'status': 'success', 'message': 'Removed comment', 'resource_id': comment_id}
    LOG.debug(data)
    activity = Activity(user_id, "DELETE_COMMENT", data)
    add_activity(activity)
    return make_response(jsonify(data), status_code)
