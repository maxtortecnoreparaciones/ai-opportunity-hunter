---
title: "[SCRAPER] Crear normalizador de datos de scrapers"
labels: ["scraper", "data"]
milestone: "Fase 2 - Scrapers"
---

## Descripción

Crear un normalizador que unifique los datos provenientes de diferentes scrapers en un formato común.

Cada portal puede tener nombres de campos distintos o formatos diferentes. El normalizador debe convertir todo a un esquema unificado.

## Criterios de aceptación

- [ ] Definir esquema unificado de salida
- [ ] Normalizar datos de LinkedIn, Wellfound y GetOnBoard
- [ ] Limpiar texto (HTML tags, espacios extraños)
- [ ] Extraer salario como rango numérico cuando sea posible
- [ ] Clasificar tipo de empleo (remoto/híbrido/presencial)

## Esquema de salida

```python
@dataclass
class NormalizedJobOffer:
    empresa: str
    cargo: str
    ubicacion: str
    salario_min: str | None
    salario_max: str | None
    moneda: str | None
    link: str
    descripcion: str
    fuente: str  # 'linkedin' | 'wellfound' | 'getonboard'
    tipo_empleo: str  # 'remoto' | 'hibrido' | 'presencial'
    fecha_publicacion: str | None
```

## Tiempo estimado

2 horas
