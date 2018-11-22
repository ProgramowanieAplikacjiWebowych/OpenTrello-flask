from modules.database.base import Session

def add_board(board):
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
