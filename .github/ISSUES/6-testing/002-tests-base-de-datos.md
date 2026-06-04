---
title: "[TEST] Tests de integración para base de datos y repositorios"
labels: ["test", "database"]
milestone: "Fase 6 - Testing"
---

## Descripción

Escribir tests de integración para los repositorios usando una base de datos de prueba (PostgreSQL test container o SQLite).

## Criterios de aceptación

- [ ] Test: guardar y recuperar JobOffer
- [ ] Test: evitar duplicados por link único
- [ ] Test: guardar y recuperar análisis por oferta
- [ ] Test: buscar ofertas por score range
- [ ] Test: perfil de usuario completo CRUD
- [ ] Test: relaciones entre entidades (FKs)
- [ ] Configurar base de datos de prueba (SQLite para CI / PostgreSQL test container)
- [ ] Cleanup de datos entre tests

## Tiempo estimado

3 horas
