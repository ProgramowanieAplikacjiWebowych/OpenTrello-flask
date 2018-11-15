from modules.database.entities.ot_board_t import Board
from modules.database.base import Session


def find_board_by_board_id(id):
    session = Session()
    result = session.query(Board).filter_by(id=id).first()
    return result

def find_all_boards():
    session = Session()
    result = session.query(Board).all()
    return result
