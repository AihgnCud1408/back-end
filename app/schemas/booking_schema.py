from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class BookingStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class BookingCreateSchema(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime

class BookingReadSchema(BaseModel):
    id: int
    user_code: int
    room_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
