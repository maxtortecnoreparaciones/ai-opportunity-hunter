---
title: "[DB] Setup PostgreSQL + SQLAlchemy"
labels: ["database", "infrastructure"]
milestone: "Fase 3 - Base de Datos"
---

## Descripción

Configurar la conexión a PostgreSQL y SQLAlchemy para el proyecto.

## Criterios de aceptación

- [ ] Configurar SQLAlchemy async engine
- [ ] Configurar session factory con patrón de dependency injection
- [ ] Variables de entorno para DATABASE_URL
- [ ] Script de migración inicial
- [ ] Docker Compose para PostgreSQL local

## Estructura esperada

```python
# backend/database/session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
```

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: opportunity_hunter
    ports:
      - "5432:5432"
```

## Tiempo estimado

2 horas
