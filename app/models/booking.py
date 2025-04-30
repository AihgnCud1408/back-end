from sqlalchemy import Column, Integer, ForeignKey, DateTime, TIMESTAMP, Enum, func
import enum
from app.db.session import Base

class BookingStatus(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_code = Column(Integer, ForeignKey("users.user_code"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.active)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
