from modules.database.base import Session
from modules.database.crud.crud_user import find_user_by_username
from modules.database.models.ot_board_t import Board


def find_board_by_board_id(id):
    session = Session()
    result = session.query(Board).filter_by(id=id).first()
    session.close()
    return result


def find_boards_by_username(username):
    session = Session()
    user = find_user_by_username(username)
    if user is not None:
        return session.query(Board).filter_by(user_id=user.id).all()


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
