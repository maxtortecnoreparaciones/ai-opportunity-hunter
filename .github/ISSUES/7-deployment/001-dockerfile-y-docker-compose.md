---
title: "[DEPLOY] Crear Dockerfile y docker-compose.yml"
labels: ["deployment", "docker"]
milestone: "Fase 7 - Despliegue"
---

## Descripción

Crear la configuración de Docker para el proyecto: Dockerfile multi-etapa y docker-compose.yml con todos los servicios.

## Criterios de aceptación

- [ ] `Dockerfile` multi-etapa (build + runtime)
- [ ] Instalar Playwright y Chromium en el contenedor
- [ ] `docker-compose.yml` con servicios: app, postgres
- [ ] Volumen persistente para PostgreSQL
- [ ] Variables de entorno mapeadas desde `.env`
- [ ] Healthcheck para base de datos
- [ ] `.dockerignore` para excluir archivos innecesarios

## Tiempo estimado

2 horas
