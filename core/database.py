from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

from models.user import User
from models.contact import Contact

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
