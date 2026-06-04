# Setup — AI Opportunity Hunter

## Requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)
- Playwright (se instala vía pip)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ai-opportunity-hunter.git
cd ai-opportunity-hunter
```

### 2. Entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar navegadores Playwright

```bash
playwright install chromium
```

### 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env`:

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/opportunity_hunter

# Gemini API
GEMINI_API_KEY=tu-api-key-aqui

# Telegram
TELEGRAM_BOT_TOKEN=tu-bot-token-aqui
TELEGRAM_CHAT_ID=tu-chat-id-aqui

# Scrapers
SCRAPE_LINKEDIN=true
SCRAPE_WELLFOUND=true
SCRAPE_GETONBOARD=true

# Scoring
SCORE_THRESHOLD=7.0
```

### 6. Base de datos

```bash
# Crear base de datos
createdb opportunity_hunter

# Ejecutar migraciones
python -m backend.database.migrate
```

### 7. Ejecutar

```bash
# Scraper básico (MVP #1) - sin IA, sin Telegram
python -m backend.scrapers.main --output data/ofertas.csv

# Pipeline completo
python -m main
```

### Docker (alternativa)

```bash
docker build -t ai-opportunity-hunter .
docker run --env-file .env ai-opportunity-hunter
```

## Variables de Entorno

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| DATABASE_URL | Sí | URL de conexión a PostgreSQL |
| GEMINI_API_KEY | Sí (con IA) | API key de Google Gemini |
| TELEGRAM_BOT_TOKEN | Sí (con Telegram) | Token del bot de Telegram |
| TELEGRAM_CHAT_ID | Sí (con Telegram) | Chat ID del usuario |
| SCORE_THRESHOLD | No | Umbral mínimo de score para notificar (default: 7.0) |
| SCRAPE_LINKEDIN | No | Activar scraper LinkedIn (default: true) |
| SCRAPE_WELLFOUND | No | Activar scraper Wellfound (default: true) |
| SCRAPE_GETONBOARD | No | Activar scraper GetOnBoard (default: true) |
