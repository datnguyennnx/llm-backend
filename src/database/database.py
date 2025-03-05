from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.content_repository import setup_database  # Import setup_database

sync_engine = create_engine(settings.DATABASE_URL)
async_engine = create_async_engine(settings.DATABASE_URL)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncSessionLocal = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine)


def get_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

def init_db():
    setup_database(sync_engine) # Initialize database using setup_database function