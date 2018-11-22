from modules.database.base import Session
from modules.database.models.ot_user_t import User


def find_user_by_username(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user
