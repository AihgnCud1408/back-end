from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.models.booking import Booking, BookingStatus
from app.models.checkin import CheckinLog
from app.models.room import Room, RoomStatus
from app.observers.subject import event_subject

class CheckinService:
    @staticmethod
    def check_in(db: Session, user_code: int, booking_id: int) -> CheckinLog:
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_code == user_code,
            Booking.status == BookingStatus.active
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found or not active")

        now = datetime.now()
        if now < booking.start_time:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Chưa đến thời gian check-in")
        # checkin_deadline = booking.start_time + timedelta(minutes=30)
        # if now > checkin_deadline:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, "Đã quá thời gian check-in")

        log = CheckinLog(booking_id=booking_id, checkin_time=now)
        db.add(log)

        room = db.query(Room).get(booking.room_id)
        room.status = RoomStatus.in_use

        db.commit()
        db.refresh(log)

        event_subject.notify(db, "checked_in", {"room_id": booking.room_id})

        return log

    @staticmethod
    def check_out(db: Session, user_code: int, booking_id: int) -> CheckinLog:
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_code == user_code
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found or not active")

        log = db.query(CheckinLog).filter(
            CheckinLog.booking_id == booking.id,
            CheckinLog.checkout_time == None
        ).first()
        if not log:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Check-in not found")

        now = datetime.now(timezone.utc)
        log.checkout_time = now

        booking.status = BookingStatus.completed
        room = db.query(Room).get(booking.room_id)
        room.status = RoomStatus.available

        db.commit()
        db.refresh(log)
        return log
