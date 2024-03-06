from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends
from app.db.database import SessionLocal

def get_db() -> any:    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]        