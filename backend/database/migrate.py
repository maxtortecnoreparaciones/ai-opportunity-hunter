from sqlalchemy import create_engine
from backend.database.base import Base
from backend.database.models import User, Profile, JobOffer, Analysis, Notification
from backend.config import settings


def run_migrations():
    sync_url = settings.database_url.replace("+asyncpg", "").replace("+aiosqlite", "")
    engine = create_engine(sync_url)
    Base.metadata.create_all(bind=engine)
    print("Migraciones ejecutadas correctamente")


if __name__ == "__main__":
    run_migrations()
