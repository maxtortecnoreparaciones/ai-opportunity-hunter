---
title: "[DB] Implementar Repository Pattern para acceso a datos"
labels: ["database", "pattern"]
milestone: "Fase 3 - Base de Datos"
---

## Descripción

Implementar el patrón Repository para abstraer el acceso a datos de cada entidad.

## Criterios de aceptación

- [ ] `JobOfferRepository`: save, find_by_link, find_all, find_by_score
- [ ] `ProfileRepository`: save, find_by_user, update
- [ ] `AnalysisRepository`: save, find_by_offer, find_top_scores
- [ ] `UserRepository`: save, find_by_telegram_id
- [ ] `NotificationRepository`: save, find_pending
- [ ] Todos los métodos deben ser asíncronos
- [ ] Inyección de dependencia de la sesión

## Estructura esperada

```python
# backend/database/repositories/job_offer_repository.py
class JobOfferRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, offer: JobOffer) -> JobOffer: ...
    async def find_by_link(self, link: str) -> JobOffer | None: ...
    async def find_all(self) -> list[JobOffer]: ...
```

## Tiempo estimado

3 horas
