from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base

class Clan(Base):
    __tablename__ = "clans"

    # UUID'yi primary key olarak kullanıyoruz
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False)
    # Created_at UTC olmalı
    created_at = Column(DateTime, default=datetime.utcnow)