from pydantic import BaseModel
from enum import Enum

class RoomType(str, Enum):
    individual = "individual"
    group = "group"
    mentoring = "mentoring"

class RoomStatus(str, Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"

class RoomReadSchema(BaseModel):
    id: int
    room_code: str
    room_type: RoomType
    location: str
    status: RoomStatus

    class Config:
        from_attributes = True