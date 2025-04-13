from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.base import Base
from utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

MAGENTA = "\033[35m"
RESET = "\033[0m"

DB_USERNAME = "root" # os.getenv("DB_USERNAME")
DB_PASSWORD = "" # os.getenv("DB_PASSWORD")
DB_SERVER = "localhost:3333"  # os.getenv("DB_SERVER")
DB_NAME = "order_payment_service_db"# os.getenv("DB_NAME")

# For MySQL with asyncio support
ASYNC_SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
SYNC_SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"

# Create both sync and async engines
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

# Synchronous engine for metadata operations (table creation)
from sqlalchemy import create_engine
sync_engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL, echo=True)

async def get_db():
    """Async database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

try:
    from models.models import *

    # Use synchronous engine for metadata operations
    Base.metadata.create_all(bind=sync_engine)
    print(f"{MAGENTA}Database order-payment service connected and tables created.{RESET}")
    print(f"{MAGENTA}Connection established successfully.{RESET}")
except Exception as e:
    logger.error(f"Database connection error: {e}")
    print(f"{MAGENTA}Database Error: {e}{RESET}")
