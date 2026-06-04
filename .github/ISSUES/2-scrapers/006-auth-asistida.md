---
title: "[AUTH] Sistema de Autenticación Asistida con Navegador"
labels: ["auth", "playwright", "high"]
milestone: "Fase 2 - Autenticación"
---

## Objetivo

Permitir que el usuario inicie sesión manualmente en plataformas de empleo y que el sistema reutilice la sesión para búsquedas y aplicaciones futuras.

## Problema

Muchas plataformas detectan automatización cuando se intentan realizar logins automáticos.

## Solución

Implementar un flujo de autenticación asistida utilizando Playwright.

## Flujo

1. El usuario ejecuta: `python -m backend.scripts.auth_cli login linkedin`
2. El sistema abre un navegador visible apuntando a la página de login
3. El usuario inicia sesión manualmente (elige Google, email, etc.)
4. Al presionar Enter, Playwright guarda cookies + storage state
5. Las próximas ejecuciones del scraper reutilizan la sesión guardada automáticamente

## Plataformas objetivo

- [ ] LinkedIn
- [ ] Wellfound (AngelList)
- [ ] GetOnBoard
- [ ] Computrabajo
- [ ] Indeed

## Criterios de aceptación

- [ ] `python -m backend.scripts.auth_cli login linkedin` abre navegador visible
- [ ] Usuario puede iniciar sesión manualmente
- [ ] Cookies se almacenan en `data/sessions/<plataforma>_session.json`
- [ ] `python -m backend.scripts.auth_cli status` muestra sesiones activas
- [ ] `python -m backend.scripts.auth_cli delete <plataforma>` elimina sesión
- [ ] Scrapers cargan sesión automáticamente si existe (fallback a anónimo si no)
- [ ] Sesión funciona para al menos una plataforma (LinkedIn o GetOnBoard)

## Archivos involucrados

- `backend/auth/session.py` — Storage state JSON
- `backend/auth/authenticator.py` — Clase base
- `backend/auth/linkedin_auth.py` — Auth LinkedIn
- `backend/auth/wellfound_auth.py` — Auth Wellfound
- `backend/auth/getonboard_auth.py` — Auth GetOnBoard
- `backend/auth/scraper_mixin.py` — Mixin para scrapers autenticados
- `backend/scripts/auth_cli.py` — CLI de autenticación
- `backend/scrapers/base.py` — Actualizado para usar mixin

## Tiempo estimado

6 horas
