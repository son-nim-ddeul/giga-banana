from sqlalchemy import Column, Integer, String, DateTime, Text, Index

from src.database.session import Base


class Session(Base):
    __tablename__ = 'sessions'
    app_name = Column(String(128), nullable=False)
    user_id = Column(String(128), nullable=False)
    id = Column(String(128), primary_key=True)
    state = Column(Text, nullable=False)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

# id, user_id, session_id, timestamp, event_data : jsonb
class Event(Base):
    __tablename__ = 'events'
    
    id = Column(String(128), primary_key=True)
    user_id = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    event_data = Column(Text, nullable=False)