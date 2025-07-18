from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    doc_type = Column(String)
    content = Column(String)
    meta = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)