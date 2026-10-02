from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class WorkOrderCreate(BaseModel):
    machine_id: int
    title: str
    description: str
    priority: str = 'low'

class WorkOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None

class TransitionRequest(BaseModel):
    new_status: str
    technician_id: Optional[int] = None
    comment: Optional[str] = None

class WorkOrderResponse(BaseModel):
    id: int
    machine_id: int
    technician_id: Optional[int]
    title: str
    description: str
    status: str
    priority: str
    opened_at: datetime
    assigned_at: Optional[datetime]
    in_progress_at: Optional[datetime]
    closed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    machine_name: str
    technician_name: Optional[str]
    message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class WorkOrderListResponse(BaseModel):
    work_orders: List[WorkOrderResponse]
    total: int
