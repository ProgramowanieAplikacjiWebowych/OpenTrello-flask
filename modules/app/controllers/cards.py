import os

from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.app.controllers.auth import auth_required
from modules.database.crud.crud_activity import add_activity
from modules.database.crud.crud_card import add_card, update_card, find_card_by_card_id
from modules.database.models.ot_activity_t import Activity
from modules.database.models.ot_card_t import Card

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/card', methods=['POST'])
@auth_required
def create_card(user_id):
    payload = request.get_json()
    card = Card.deserialize(payload)
    status_code, card_id = add_card(card)
    data = {'status': 'success', 'message': 'Created new card', 'resource_id': card_id}
    LOG.debug(card)
    activity = Activity(user_id, "CREATE_CARD", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<id>/card', methods=['PUT'])
@auth_required
def modify_card(user_id, id):
    payload = request.get_json()
    card = Card.deserialize(payload)
    card.id = id
    status_code, card_id = update_card(card)
    data = {'status': 'success', 'message': 'Updated card', 'resource_id': card_id}
    LOG.debug(card)
    activity = Activity(user_id, "MODIFY_CARD", payload)
    add_activity(activity)
    return make_response(jsonify(data), status_code)


@app.route('/<id>/card/archive', methods=['PUT'])
@auth_required
def archive_card(user_id, id):
    card = find_card_by_card_id(id)
    card.active = 0
    status_code, card_id = update_card(card)
    data = {'status': 'success', 'message': 'Archived card', 'resource_id': card.id}
    LOG.debug(card)
    activity = Activity(user_id, "ARCHIVE_CARD", card)
    add_activity(activity)
    return make_response(jsonify(data), status_code)
