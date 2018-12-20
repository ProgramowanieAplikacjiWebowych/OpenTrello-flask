from modules.database.base import Session
from modules.database.crud.crud_user import find_user_by_username
from modules.database.models.ot_board_t import Board


def find_board_by_board_id(id):
    session = Session()
    result = session.query(Board).filter_by(id=id, active=1).first()
    session.close()
    return result


def find_boards_by_username(username):
    session = Session()
    user = find_user_by_username(username)
    if user is not None:
        result = session.query(Board).filter_by(user_id=user.id, active=1).all()
        session.close()
        return result
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
