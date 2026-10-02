from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models.work_order import WorkOrder
from app.models.comment import Comment
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate, TransitionRequest, WorkOrderResponse, WorkOrderListResponse
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.state_machine import validate_transition, TransitionError

router = APIRouter(prefix="/api/work-orders", tags=["Work Orders"])

def utcnow():
    return datetime.now(timezone.utc)

def build_wo_response(wo: WorkOrder, message: str = None) -> dict:
    d = {c.name: getattr(wo, c.name) for c in wo.__table__.columns}
    d['machine_name'] = wo.machine.name if wo.machine else "Unknown"
    d['technician_name'] = wo.technician.name if wo.technician else None
    if message:
        d['message'] = message
    return d

@router.post("/", response_model=WorkOrderResponse)
def create_work_order(wo: WorkOrderCreate, db: Session = Depends(get_db)):
    db_wo = WorkOrder(
        machine_id=wo.machine_id,
        title=wo.title,
        description=wo.description,
        priority=wo.priority,
        status="open",
        opened_at=utcnow()
    )
    db.add(db_wo)
    db.commit()
    db.refresh(db_wo)
    return build_wo_response(db_wo)

@router.get("/", response_model=WorkOrderListResponse)
def list_work_orders(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    machine_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(WorkOrder)
    if status:
        query = query.filter(WorkOrder.status == status)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if machine_id:
        query = query.filter(WorkOrder.machine_id == machine_id)
        
    wos = query.all()
    total = len(wos)
    
    priority_map = {'critical': 1, 'high': 2, 'low': 3}
    wos.sort(key=lambda x: (priority_map.get(x.priority, 99), x.opened_at))
    
    return {"work_orders": [build_wo_response(wo) for wo in wos], "total": total}

@router.get("/{id}", response_model=WorkOrderResponse)
def get_work_order(id: int, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return build_wo_response(wo)

@router.put("/{id}", response_model=WorkOrderResponse)
def update_work_order(id: int, updates: WorkOrderUpdate, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    if updates.title is not None:
        wo.title = updates.title
    if updates.description is not None:
        wo.description = updates.description
    if updates.priority is not None:
        wo.priority = updates.priority
        
    db.commit()
    db.refresh(wo)
    return build_wo_response(wo)

@router.delete("/{id}")
def delete_work_order(id: int, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    db.delete(wo)
    db.commit()
    return {"message": "deleted"}

@router.post("/{id}/transition", response_model=WorkOrderResponse)
def transition_work_order(id: int, req: TransitionRequest, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
        
    try:
        validate_transition(wo.status, req.new_status)
    except TransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if req.new_status == 'assigned':
        if not req.technician_id and not wo.technician_id:
            raise HTTPException(status_code=400, detail="technician_id is required for assigned status")
        if req.technician_id:
            wo.technician_id = req.technician_id
        wo.assigned_at = utcnow()
    elif req.new_status == 'in_progress':
        wo.in_progress_at = utcnow()
    elif req.new_status == 'closed':
        wo.closed_at = utcnow()
        
    wo.status = req.new_status
    
    if req.comment:
        new_comment = Comment(work_order_id=wo.id, author="System/User", body=req.comment)
        db.add(new_comment)
        
    db.commit()
    db.refresh(wo)
    return build_wo_response(wo, message=f"Transitioned to {req.new_status}")

@router.post("/{id}/comments", response_model=CommentResponse)
def create_comment(id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    new_comment = Comment(work_order_id=id, author=comment.author, body=comment.body)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{id}/comments", response_model=List[CommentResponse])
def get_comments(id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.work_order_id == id).order_by(Comment.created_at.asc()).all()
    return comments
