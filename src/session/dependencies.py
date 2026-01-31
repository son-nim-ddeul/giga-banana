from typing import Generator
from src.database.session import get_rds_db
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    yield from get_rds_db()
