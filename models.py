import reflex as rx
import enum
import os

from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Role(enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
    password = Column(String, nullable=False)

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    f_name = Column(String, nullable = False)
    l_name = Column(String, nullable = False)
    start_date = Column(String, nullable = False)
    end_date = Column(String, nullable = False)
    reson = Column(String)

DB_URL = "sqlite:///dayoff/data.db"
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    os.makedirs("dayoff", exist_ok=True)
    Base.metadata.create_all(bind=engine)
