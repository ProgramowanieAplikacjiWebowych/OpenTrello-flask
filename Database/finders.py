from Database.base import Session
from Database.Entities.ot_list_t import List
from Database.Entities.ot_board_t import Board

session = Session()

def find_lists_by_board_id(board_id):
    result = session.query(List).filter_by(board_id=board_id)
    return result

def find_board_by_board_id(id):
    result = session.query(Board).filter_by(id=id).first()
    return result

def find_all_boards():
    result = session.query(Board).all()
    return result