# Requisitos del Sistema — AI Opportunity Hunter

## Requisitos Funcionales

### Módulo de Scraping (RF-01 a RF-05)

| ID    | Descripción | Prioridad |
|-------|-------------|-----------|
| RF-01 | El sistema debe extraer ofertas de empleo desde LinkedIn | Alta |
| RF-02 | El sistema debe extraer ofertas de empleo desde Wellfound (AngelList) | Alta |
| RF-03 | El sistema debe extraer ofertas de empleo desde GetOnBoard | Alta |
| RF-04 | El sistema debe extraer: empresa, cargo, ubicación, salario, link y descripción | Alta |
| RF-05 | El sistema debe guardar los resultados en un archivo CSV como fallback | Media |

### Módulo de Base de Datos (RF-06 a RF-08)

| ID    | Descripción | Prioridad |
|-------|-------------|-----------|
| RF-06 | El sistema debe almacenar ofertas en PostgreSQL | Alta |
| RF-07 | El sistema debe evitar duplicados por link único | Alta |
| RF-08 | El sistema debe permitir almacenar perfiles de usuario | Media |

### Módulo de IA (RF-09 a RF-11)

| ID    | Descripción | Prioridad |
|-------|-------------|-----------|
| RF-09 | El sistema debe analizar cada oferta usando Gemini API | Alta |
| RF-10 | El sistema debe calcular un score de compatibilidad (0-10) | Alta |
| RF-11 | El sistema debe generar fortalezas y debilidades por oferta | Media |

### Módulo de Notificaciones (RF-12 a RF-14)

| ID    | Descripción | Prioridad |
|-------|-------------|-----------|
| RF-12 | El sistema debe enviar notificaciones vía Telegram | Alta |
| RF-13 | El sistema debe notificar solo ofertas con score >= umbral configurable | Media |
| RF-14 | El sistema debe incluir empresa, cargo y score en la notificación | Alta |

### Módulo de Seguimiento (RF-15)

| ID    | Descripción | Prioridad |
|-------|-------------|-----------|
| RF-15 | El sistema debe registrar aplicaciones realizadas para evitar re-aplicar | Baja |

## Requisitos No Funcionales

| ID    | Descripción | Categoría |
|-------|-------------|-----------|
| RNF-01 | El scraper debe completar una ejecución en < 10 minutos | Rendimiento |
| RNF-02 | El análisis IA debe responder en < 30 segundos por oferta | Rendimiento |
| RNF-03 | Los datos sensibles (API keys) deben estar en variables de entorno | Seguridad |
| RNF-04 | El sistema debe ejecutarse en contenedores Docker | Portabilidad |
| RNF-05 | El código debe seguir el patrón Repository + Service Layer | Mantenibilidad |
| RNF-06 | Debe existir cobertura de pruebas unitarias >= 70% | Calidad |
| RNF-07 | La base de datos debe ser PostgreSQL 15+ | Compatibilidad |
| RNF-08 | El scraper debe respetar robots.txt y rate limiting | Ética |
