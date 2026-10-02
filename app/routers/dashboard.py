from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.kpi import get_dashboard_stats
from app.schemas.dashboard import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)
