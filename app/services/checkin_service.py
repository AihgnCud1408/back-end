from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.models.booking import Booking, BookingStatus
from app.models.checkin import CheckinLog
from app.models.room import Room, RoomStatus
from app.schemas.checkin_schema import CheckinReadSchema
from app.observers.subject import event_subject

class CheckinService:
    @staticmethod
    def check_in(db: Session, user_id: str, booking_id: int):
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == BookingStatus.active
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found or not active")

        now = datetime.now()
        if now < booking.start_time:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Chưa đến thời gian check-in")

        log = CheckinLog(booking_id=booking_id, checkin_time=now)
        db.add(log)

        room = db.query(Room).filter(Room.id == booking.room_id).first()
        room.status = RoomStatus.in_use

        db.commit()
        db.refresh(log)

        event_subject.notify("checked_in", {"room_id": booking.room_id})

        return CheckinReadSchema(
            id=log.id,
            booking_id=booking.id,
            room_code=room.room_code,
            checkin_time=log.checkin_time,
            checkout_time=None
        )

    @staticmethod
    def check_out(db: Session, user_id: str, booking_id: int):
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_id == user_id
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found or not active")

        log = db.query(CheckinLog).filter(
            CheckinLog.booking_id == booking.id,
            CheckinLog.checkout_time == None
        ).first()
        if not log:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Check-in not found")

        now = datetime.now()
        log.checkout_time = now

        booking.status = BookingStatus.completed
        room = db.query(Room).get(booking.room_id)
        room.status = RoomStatus.available

        db.commit()
        db.refresh(log)
        return CheckinReadSchema(
            id=log.id,
            booking_id=booking.id,
            room_code=room.room_code,
            checkin_time=log.checkin_time,
            checkout_time=log.checkout_time
        )
