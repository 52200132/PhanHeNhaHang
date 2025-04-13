from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.base import Base
from utils.logger import get_logger

load_dotenv()

MAGENTA = "\033[35m"
RESET = "\033[0m"

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

# Cấu hình kết nối đồng bộ cho MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"

# Tạo engine đồng bộ
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    from models.models import *

    # Khởi tạo cơ sở dữ liệu
    Base.metadata.create_all(bind=engine)
    print(f"{MAGENTA}Database order-payment service connected and tables created.{RESET}")
    print(f"{MAGENTA}Connection established successfully.{RESET}")
except Exception as e:
    print(f"{MAGENTA}Database Error: {e}{RESET}")
