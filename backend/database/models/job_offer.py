from sqlalchemy import Column, Integer, String, Text, DateTime, Date, func
from backend.database.base import Base


class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=False)
    ubicacion = Column(String(255), default="")
    salario_min = Column(String(50), nullable=True)
    salario_max = Column(String(50), nullable=True)
    moneda = Column(String(10), nullable=True)
    link = Column(Text, unique=True, nullable=False)
    descripcion = Column(Text, default="")
    fuente = Column(String(50), default="")
    tipo_empleo = Column(String(20), default="")
    fecha_publicacion = Column(Date, nullable=True)
    encontrado_en = Column(DateTime, server_default=func.now())
