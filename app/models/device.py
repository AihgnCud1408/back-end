from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import enum
from app.db.session import Base

class DeviceType(str, enum.Enum):
    light = "light"
    fan = "fan"
    air_conditioner = "air_conditioner"

class DeviceStatus(str, enum.Enum):
    on = "on"
    off = "off"
    error = "error"

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(DeviceType), nullable=False)
    status = Column(Enum(DeviceStatus), nullable=False, default=DeviceStatus.off)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
