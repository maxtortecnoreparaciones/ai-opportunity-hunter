---
title: "[DB] Crear modelos SQLAlchemy (User, Profile, JobOffer, Analysis, Notification)"
labels: ["database", "models"]
milestone: "Fase 3 - Base de Datos"
---

## Descripción

Implementar los modelos SQLAlchemy para todas las entidades del sistema.

## Criterios de aceptación

- [ ] Modelo `User` con campos: id, nombre, email, telegram_chat_id
- [ ] Modelo `Profile` con campos: id, user_id, tecnologias, experiencia, nivel_ingles, seniority
- [ ] Modelo `JobOffer` con campos: id, empresa, cargo, ubicacion, salario, link (UNIQUE), descripcion, fuente
- [ ] Modelo `Analysis` con campos: id, job_offer_id, profile_id, score, fortalezas, debilidades, recomendacion
- [ ] Modelo `Notification` con campos: id, analysis_id, user_id, tipo, estado
- [ ] Relaciones entre modelos (FKs)
- [ ] Índices en link, score, profile_id

## Estructura esperada

```python
# backend/database/models/
# ├── __init__.py
# ├── user.py
# ├── profile.py
# ├── job_offer.py
# ├── analysis.py
# └── notification.py
```

## Tiempo estimado

2 horas
