from modules.database.base import Session
from modules.database.models.ot_activity_t import Activity


def add_activity(activity):
    if not isinstance(activity, Activity):
        return
    status_code = 201
    session = Session()
    try:
        session.add(activity)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = activity.id
        session.close()
    return status_code, id
