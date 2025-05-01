from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.booking import Booking

class CheckinLog(Base):
    __tablename__ = 'checkin_logs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    checkin_time = Column(DateTime, server_default=func.now())
    checkout_time = Column(DateTime, nullable=True)
