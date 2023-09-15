from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Create an SQLite in-memory database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define an SQLAlchemy model for the database
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)

class Item_Pydantic(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True

class Item_Pydantic_Update(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



