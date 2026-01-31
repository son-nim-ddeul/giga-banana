from sqlalchemy.orm import Session
from .models import Session


def get_single_session(db: Session, session_id: str):
    return db.query(Session).filter(Session.id == session_id).first()

def get_list_sessions(db: Session, user_id: str):
    return db.query(Session).filter(Session.user_id == user_id).all()