# import sqlite_vec
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings

Base = declarative_base()

# RDS Engine
# PostgreSQL 연결 설정
rds_engine = create_engine(
    f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}",
    pool_pre_ping=True,  # 연결이 유효한지 확인
    pool_size=5,  # 기본 연결 풀 크기
    max_overflow=10,  # 추가로 생성 가능한 최대 연결 수
    pool_recycle=3600,  # 1시간 후 연결 재활용 (PostgreSQL timeout 방지)
    echo=False,  # SQL 쿼리 로깅 (개발 시 True로 설정 가능)
)
RDS_Session = sessionmaker(
    autocommit=False, autoflush=False, bind=rds_engine)

def get_rds_db():
    db = RDS_Session()
    try:
        yield db
    finally:
        db.close()

