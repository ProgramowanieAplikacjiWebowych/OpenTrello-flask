from modules.database.base import Session
from modules.database.models.ot_user_t import User


def find_user_by_username(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user


def find_user_by_email(email):
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    return user


def find_user_by_id(id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    session.close()
    return user


def add_user(user):
    if not isinstance(user, User):
        return None
    status_code = 201
    session = Session()
    try:
        session.add(user)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = user.id
        session.close()
    return status_code, id
