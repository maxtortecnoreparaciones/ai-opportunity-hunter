from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from backend.database.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tecnologias = Column(Text, nullable=False)
    experiencia_anos = Column(Integer, default=0)
    nivel_ingles = Column(String(20), default="")
    seniority = Column(String(50), default="")
    created_at = Column(DateTime, server_default=func.now())
