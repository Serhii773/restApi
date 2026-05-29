import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:mysecretpassword@localhost:5432/library"
)

# Створюємо двигун (engine) для підключення
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створюємо фабрику сесій (через неї ми будемо робити запити до БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для всіх наших майбутніх моделей (таблиць)
Base = declarative_base()

# Функція-залежність (Dependency), яка буде видавати сесію для кожного запиту
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()