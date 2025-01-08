# usage_db.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///vton_usage.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

class UsageRecord(Base):
    __tablename__ = "usage_records"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, index=True)
    usage_count = Column(Integer)

def init_db():
    Base.metadata.create_all(bind=engine)
