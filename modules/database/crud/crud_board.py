from flask.json import jsonify
import json

from modules.database.crud.crud_list import find_lists_by_board_id
from modules.database.base import Session
from modules.database.crud.crud_card import find_cards_by_list_id
from modules.database.crud.crud_user import find_user_by_username
from modules.database.models.board_with_related_data import BoardWithRelatedData
from modules.database.models.list_with_related_data import ListWihtRelatedData
from modules.database.models.ot_board_t import Board


def find_board_with_related_data_by_board_id(id):
    session = Session()
    board = session.query(Board).filter_by(id=id, active=1).first()

    lists = find_lists_by_board_id(id)

    lists_with_cards = []
    for li in lists:

        cards = find_cards_by_list_id(li.id)
        # cards = cards.serialize()
        cardss = []
        for card in cards:
            di = card.serialize()
            cardss.append(di)

        lisss = ListWihtRelatedData(li.id, li.name, cardss)
        lisss = lisss.to_json()
        lists_with_cards.append(lisss)

    all_data = BoardWithRelatedData(board.id, board.name, board.bg_color, lists_with_cards)

    session.close()
    return all_data


def find_boards_by_username(username):
    session = Session()
    user = find_user_by_username(username)
    if user is not None:
        result = session.query(Board).filter_by(user_id=user.id, active=1).all()
        session.close()
        return result
    session.close()
    return None


def find_boards_by_user_id(user_id):
    session = Session()
    result = session.query(Board).filter_by(user_id=user_id, active=1).all()
    session.close()
    return result


def add_board(board):
    if not isinstance(board, Board):
        return
    status_code = 201
    session = Session()
    try:
        session.add(board)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = board.id
        session.close()
    return status_code, id


def update_board(board):
    if not isinstance(board, Board) or board.id is None:
        return
    status_code = 200
    session = Session()
    try:
        old_card = session.query(Board).filter_by(id=board.id).first()
        old_card.name = board.name
        old_card.bg_color = board.bg_color
        old_card.active = board.active
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = board.id
        session.close()
    return status_code, id
