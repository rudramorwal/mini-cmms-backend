from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.technician import Technician
from app.schemas.technician import TechnicianResponse

router = APIRouter(prefix="/api/technicians", tags=["Technicians"])

@router.get("/", response_model=List[TechnicianResponse])
def list_technicians(db: Session = Depends(get_db)):
    return db.query(Technician).all()
