from modules.database.models.ot_list_t import List
from modules.database.base import Session


def find_lists_by_board_id(board_id):
    session = Session()
    result = session.query(List).filter_by(board_id=board_id)
    return result


def add_list(li):
    if not isinstance(li, List):
        return
    status_code = 201
    session = Session()
    try:
        session.add(li)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = li.id
        session.close()
    return status_code, id


def update_list(li):
    if not isinstance(li, List) or li.id is None:
        return
    status_code = 200
    session = Session()
    try:
        old_list = session.query(List).filter_by(id=li.id).first()
        old_list.name = li.name
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = li.id
        session.close()
    return status_code, id
