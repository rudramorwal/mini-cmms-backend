from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentCreate(BaseModel):
    author: str
    body: str

class CommentResponse(BaseModel):
    id: int
    work_order_id: int
    author: str
    body: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
