from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database/historical_data.db" 

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() :
    db = SessionLocal()
    try : 
        return db 
    finally : 
        db.close()