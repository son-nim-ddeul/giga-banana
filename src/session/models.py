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

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(String(128), primary_key=True)
    app_name = Column(String(128), nullable=False)
    user_id = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=False, index=True)
    invocation_id = Column(String(256), nullable=False)
    author = Column(String(256), nullable=False)
    branch = Column(String(256), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    content = Column(Text, nullable=True)
    actions = Column(Text, nullable=True)
    long_running_tool_ids_json = Column(Text, nullable=True)
    grounding_metadata = Column(Text, nullable=True)
    partial = Column(Integer, nullable=True)  # tinyint(1) → Integer
    turn_complete = Column(Integer, nullable=True)  # tinyint(1) → Integer
    error_code = Column(String(256), nullable=True)
    error_message = Column(String(1024), nullable=True)
    interrupted = Column(Integer, nullable=True)  # tinyint(1) → Integer
    custom_metadata = Column(Text, nullable=True)
    
    __table_args__ = (
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )