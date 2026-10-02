from pydantic import BaseModel, ConfigDict
from typing import Optional

class TechnicianResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    specialization: Optional[str]
    is_available: bool

    model_config = ConfigDict(from_attributes=True)
