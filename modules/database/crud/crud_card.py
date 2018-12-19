from modules.database.base import Session
from modules.database.models.ot_card_t import Card


def add_card(card):
    if not isinstance(card, Card):
        return
    status_code = 201
    session = Session()
    try:
        session.add(card)
    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = card.id
        session.close()
    return status_code, id


def update_card(card):
    if not isinstance(card, Card) or card.id is None:
        return
    status_code = 200
    session = Session()
    try:
        old_card = session.query(Card).filter_by(id=card.id).first()

        old_card.name = card.name
        old_card.description = card.description
        old_card.date_to = card.date_to

    except:
        session.rollback()
        status_code = 409
    finally:
        session.commit()
        id = card.id
        session.close()
    return status_code, id
