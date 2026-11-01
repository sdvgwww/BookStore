from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ВАЖНО: замените ВАШ_ПАРОЛЬ на пароль от PostgreSQL
DATABASE_URL = "postgresql://postgres:Katro123@localhost:5432/bookstore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()