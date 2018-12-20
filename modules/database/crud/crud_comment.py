from modules.database import Session
from modules.database.models.ot_comment_t import Comment


def find_comment_by_object_type_and_object_id(object_type, object_id):
    session = Session()
    result = session.query(Comment).filter_by(object_id=object_id, object_type=object_type).first()
    session.close()
    return result


def add_comment(comment):
    if not isinstance(comment, Comment):
        return
    status_code = 201
    session = Session()
    try:
        session.add(comment)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = comment.id
        session.close()
    return status_code, id


def update_comment(comment):
    if not isinstance(comment, Comment) or comment.id is None:
        return
    status_code = 201
    session = Session()
    try:
        old_comment = session.query(Comment).filter_by(id=comment.id).first()
        old_comment.description = comment.description
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = comment.id
        session.close()
    return status_code, id


def delete_comment(id):
    if id is None:
        return
    status_code = 201
    session = Session()
    try:
        old_comment = session.query(Comment).filter_by(id=id).first()
        session.delete(old_comment)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        session.close()
    return status_code, id
