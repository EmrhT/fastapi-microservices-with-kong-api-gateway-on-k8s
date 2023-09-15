from pydantic import BaseModel
from typing import Optional, Literal
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# Create an SQLite in-memory database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define an SQLAlchemy model for the database
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    address = Column(String)
    user_type = Column(String)

class User_Pydantic(BaseModel):
    name: str
    address: str
    user_type: Literal['supplier', 'consumer', 'admin', 'super_admin']
    class Config:
        orm_mode = True

class User_Pydantic_Update(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    user_type: Optional[Literal['supplier', 'consumer', 'admin', 'super_admin']] = None
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



