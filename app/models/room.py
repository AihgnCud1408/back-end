from sqlalchemy import Column, Integer, String, Enum
import enum
from app.db.session import Base

class RoomType(str, enum.Enum):
    individual = "individual"
    group = "group"
    mentoring = "mentoring"

class RoomStatus(str, enum.Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"

class SensorStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_code = Column(String(20), unique=True, index=True, nullable=False)
    room_type = Column(Enum(RoomType), nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(Enum(RoomStatus), nullable=False, default=RoomStatus.available)
    sensor = Column(Enum(SensorStatus), nullable=False, default=SensorStatus.inactive)