from modules.database import List
from modules.database import Session


def find_lists_by_board_id(board_id):
    session = Session()
    result = session.query(List).filter_by(board_id=board_id)
    return result
