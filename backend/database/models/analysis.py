from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from backend.database.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_offer_id = Column(Integer, ForeignKey("job_offers.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    score = Column(Float, default=0.0)
    fortalezas = Column(Text, default="")
    debilidades = Column(Text, default="")
    recomendacion = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
