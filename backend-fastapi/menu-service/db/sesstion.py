from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .base import Base

load_dotenv()

MAGENTA = '\033[35m'
RESET = '\033[0m'

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mysql")
if DATABASE_TYPE == "sqlserver":
    import pyodbc
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
else:
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
    Base.metadata.create_all(bind=engine)
    print(f"{MAGENTA}Database menu service connected and tables created.{RESET}")
    print(f"{MAGENTA}Connection established successfully.{RESET}")
except Exception as e:
    print(f"{MAGENTA}Database Error: {e}{RESET}")