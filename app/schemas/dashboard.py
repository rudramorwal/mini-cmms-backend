from pydantic import BaseModel, ConfigDict
from typing import List

class MachineMTTR(BaseModel):
    machine_id: int
    machine_name: str
    mttr_hours: float
    repair_count: int

class DashboardStats(BaseModel):
    open_work_orders: int
    total_work_orders: int
    mttr_by_machine: List[MachineMTTR]
    worst_5_machines: List[MachineMTTR]
