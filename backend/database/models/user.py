from sqlalchemy import Column, Integer, String, Text, DateTime, func
from backend.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telegram_chat_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
