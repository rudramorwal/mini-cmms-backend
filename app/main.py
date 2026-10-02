from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # noqa: F401 — registers all models with Base.metadata
from app.routers import work_orders, machines, technicians, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini CMMS", description="Maintenance Work Order Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:3000', '*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(work_orders.router)
app.include_router(machines.router)
app.include_router(technicians.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Mini CMMS API", "docs": "/docs"}
