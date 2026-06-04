"""AI Opportunity Hunter - Pipeline completo"""

import asyncio
import argparse
from backend.scrapers.main import run_pipeline as scrape_and_export
from backend.config import settings


async def full_pipeline():
    print("=== AI Opportunity Hunter ===")

    offers = await scrape_and_export()
    print(f"\nPipeline completado. {len(offers)} ofertas procesadas.")


def main():
    parser = argparse.ArgumentParser(description="AI Opportunity Hunter")
    parser.add_argument("--ai", action="store_true", help="Incluir análisis con IA")
    parser.add_argument("--notify", action="store_true", help="Enviar notificaciones Telegram")
    args = parser.parse_args()

    asyncio.run(full_pipeline())


if __name__ == "__main__":
    main()
