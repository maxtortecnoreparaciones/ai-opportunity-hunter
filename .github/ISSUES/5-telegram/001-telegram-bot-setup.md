---
title: "[TELEGRAM] Configurar bot de Telegram y enviar notificaciones"
labels: ["telegram", "notifications"]
milestone: "Fase 5 - Telegram"
---

## Descripción

Configurar un bot de Telegram que envíe notificaciones al usuario con las mejores oportunidades encontradas.

## Criterios de aceptación

- [ ] Configurar bot con `python-telegram-bot` o API directa
- [ ] Obtener y verificar token desde variable de entorno
- [ ] Enviar mensaje con formato: empresa, cargo, score, link
- [ ] Enviar solo ofertas con score >= umbral configurado
- [ ] Manejar errores de envío (timeout, chat no encontrado)

## Formato del mensaje

```
🚀 Nueva oportunidad encontrada

Empresa: MixRank
Cargo: Senior Python Developer
Score: 9.1/10
Link: https://.../apply

Fortalezas: Python, AWS, Docker
Debilidades: Kubernetes (no en perfil)
```

## Estructura esperada

```python
# backend/telegram/notifier.py
class TelegramNotifier:
    async def send_opportunity(self, scored_offer: ScoredOffer) -> bool: ...
    async def send_daily_summary(self, offers: list[ScoredOffer]) -> bool: ...
```

## Tiempo estimado

3 horas
