from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Google Cloud SQL bağlantısı için ortam değişkeninden URL alınacak
# Local test için varsayılan: sqlite:///./clans.db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clans.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Injection için veritabanı oturumu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()