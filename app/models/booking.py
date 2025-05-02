from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date, Time, Enum, func
import enum
from app.db.session import Base

class BookingStatus(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"
    checked_in = "checked_in"
    checked_out = "checked_out"

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.active)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
