---
title: "[FUTURO] Aplicación automática a vacantes"
labels: ["future", "enhancement"]
milestone: "Fase 8 - Futuro (V2)"
---

## Descripción

Implementar aplicación automática a vacantes: cuando se encuentra una oferta con score alto, el sistema navega al portal y completa la postulación automáticamente.

## Criterios de aceptación

- [ ] Auto-fill de formularios de postulación en LinkedIn Fácil Postulación
- [ ] Auto-fill en Wellfound
- [ ] Registro de aplicaciones realizadas en DB
- [ ] Validación para evitar re-aplicar a la misma oferta
- [ ] Verificación CAPTCHA detectada → notificación manual

## Flujo

```
Oferta encontrada → Analizar → Score >= 8.0 → Aplicar automáticamente → Registrar → Notificar
```

## Tiempo estimado

8 horas
