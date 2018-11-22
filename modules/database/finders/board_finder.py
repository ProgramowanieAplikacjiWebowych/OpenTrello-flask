from modules.database.base import Session
from modules.database.finders.user_finder import find_user_by_username
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
