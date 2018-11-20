from modules.database.base import Session
from modules.database.models.ot_board_t import Board
from modules.database.models.ot_user_t import User


def find_board_by_board_id(id):
    session = Session()
    result = session.query(Board).filter_by(id=id).first()
    return result

def find_boards_by_username(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user is not None:
        return session.query(Board).filter_by(user_id=user.id).all()
    else:
        return None
