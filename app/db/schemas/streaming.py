from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Streaming(Base):
    __tablename__ = "streaming_data"
    id = Column(Integer, primary_key=True)
    uri = Column(String)
    device_name = Column(String)
    create_time = Column(DateTime)
