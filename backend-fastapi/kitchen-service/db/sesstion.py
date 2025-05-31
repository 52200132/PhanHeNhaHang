from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.base import Base
from utils.logger import default_logger

logger = default_logger

load_dotenv()

MAGENTA = "\033[35m"
RESET = "\033[0m"

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME_1")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    from models.models import *

    Base.metadata.create_all(bind=engine)
    logger.info(f"Database kitchen service connected successfully to {DB_SERVER}/{DB_NAME}")
    logger.info("Database tables created or verified")
except ImportError as e:
    logger.critical(f"Failed to import models: {str(e)}")
except Exception as e:
    logger.critical(f"Database connection error: {str(e)}")
    logger.critical(f"Connection URL: {SQLALCHEMY_DATABASE_URL}")