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

class Creations(Base):
    __tablename__ = 'creations'
    
    creation_id = Column(String(128), primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    workflow = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)
    image_url = Column(String(512), nullable=False)
    created_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(10), nullable=False, default='active')