import re
from backend.models import JobOffer


class JobNormalizer:
    @staticmethod
    def normalizar(o: JobOffer) -> JobOffer:
        o.cargo = o.cargo.strip() if o.cargo else ""
        o.empresa = o.empresa.strip() if o.empresa else ""
        o.descripcion = re.sub(r"<[^>]+>", "", o.descripcion).strip()
        o.descripcion = re.sub(r"\s+", " ", o.descripcion).strip()
        o.tipo_empleo = JobNormalizer._clasificar_tipo(o.ubicacion or "")
        return o

    @staticmethod
    def _clasificar_tipo(ubicacion: str) -> str:
        ub = ubicacion.lower()
        if any(w in ub for w in ["remoto", "remote", "100% remoto"]):
            return "remoto"
        if any(w in ub for w in ["híbrido", "hibrido", "hybrid"]):
            return "hibrido"
        if any(w in ub for w in ["presencial", "onsite", "oficina"]):
            return "presencial"
        return ""
