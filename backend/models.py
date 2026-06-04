from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JobOffer:
    empresa: str
    cargo: str
    ubicacion: str
    salario_min: str | None = None
    salario_max: str | None = None
    moneda: str | None = None
    link: str = ""
    descripcion: str = ""
    fuente: str = ""
    tipo_empleo: str = ""
    fecha_publicacion: str | None = None


@dataclass
class Profile:
    tecnologias: str
    experiencia_anos: int
    nivel_ingles: str
    seniority: str
    habilidades_extra: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    score: float
    fortalezas: list[str]
    debilidades: list[str]
    recomendacion: str
