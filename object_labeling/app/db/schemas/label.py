from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Label(Base):
    __tablename__ = "label_data"
    id = Column(Integer, primary_key=True)
    streaming_data_id = Column(Integer)
    equipment_no = Column(String)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    create_time = Column(DateTime)
    type = Column(String)