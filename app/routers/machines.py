from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.machine import Machine
from app.models.work_order import WorkOrder
from app.schemas.machine import MachineResponse
from app.schemas.work_order import WorkOrderResponse
from app.routers.work_orders import build_wo_response

router = APIRouter(prefix="/api/machines", tags=["Machines"])

@router.get("/", response_model=List[MachineResponse])
def list_machines(db: Session = Depends(get_db)):
    return db.query(Machine).all()

@router.get("/{id}", response_model=MachineResponse)
def get_machine(id: int, db: Session = Depends(get_db)):
    m = db.query(Machine).filter(Machine.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Machine not found")
    return m

@router.get("/{id}/history", response_model=List[WorkOrderResponse])
def get_machine_history(id: int, search: Optional[str] = None, db: Session = Depends(get_db)):
    m = db.query(Machine).filter(Machine.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Machine not found")
        
    query = db.query(WorkOrder).filter(WorkOrder.machine_id == id)
    
    if search:
        search_term = f"%{search.lower()}%"
        # Since sqlite handles ILIKE via LIKE basically if case-insensitive, we'll use like for standard sql
        query = query.filter(
            WorkOrder.title.ilike(search_term) | WorkOrder.description.ilike(search_term)
        )
        
    wos = query.all()
    return [build_wo_response(wo) for wo in wos]
