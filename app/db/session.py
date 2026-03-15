from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from app.dependencies import get_db_credentials

Base = declarative_base()


# BASE_DIR = Path(__file__).resolve().parent.parent
# engine = create_engine(
#     f"sqlite:///{BASE_DIR}/test.db", connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


creds = get_db_credentials()
DATABASE_URL = (
    f"postgresql://{creds['username']}:{creds['password']}"
    f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ.get('DB_NAME', 'postgres')}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
