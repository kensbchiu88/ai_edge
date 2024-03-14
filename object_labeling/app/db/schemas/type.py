from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Type(Base):
    __tablename__ = "type_data"
    key = Column(String, primary_key=True)
    text = Column(String)
    create_time = Column(DateTime)