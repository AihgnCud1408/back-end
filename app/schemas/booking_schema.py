from pydantic import BaseModel
from enum import Enum
from datetime import datetime, time, date

class BookingStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    checked_in = "checked_in"
    checked_out = "checked_out"

class BookingCreateSchema(BaseModel):
    room_code: str
    booking_date: date
    start_time: time
    end_time: time

class BookingReadSchema(BaseModel):
    id: int
    user_id: int
    room_code: str
    booking_date: date
    start_time: time
    end_time: time
    status: BookingStatus
    created_at: datetime

    class Config:
        orm_mode = True
