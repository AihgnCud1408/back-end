from pydantic import BaseModel
from datetime import datetime

class CheckinCreateSchema(BaseModel):
    booking

class CheckinReadSchema(BaseModel):
    id: int
    booking_id: int
    room_code: str
    checkin_time: datetime
    checkout_time: datetime | None

    class Config:
        orm_mode = True
