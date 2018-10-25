from modules.database import Board
from modules.database import Session


def find_board_by_board_id(id):
    session = Session()
    result = session.query(Board).filter_by(id=id).first()
    return result


def find_all_boards():
    session = Session()
    result = session.query(Board).all()
    return result
