from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from backend.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tipo = Column(String(50), default="nueva_oferta")
    estado = Column(String(20), default="pending")
    sent_at = Column(DateTime, nullable=True)
