from modules.database.models.ot_list_t import List
from modules.database.base import Session


def find_lists_by_board_id(board_id):
    session = Session()
    result = session.query(List).filter_by(board_id=board_id)
    return result
