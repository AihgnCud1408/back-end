from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.booking import Booking, BookingStatus
from app.models.checkin import CheckinLog
from app.models.room import Room, RoomStatus
from app.observers.subject import event_subject

class CheckinService:
    @staticmethod
    def check_in(db: Session, user_id: int, booking_id: int):
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == BookingStatus.active
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found or not active")

        now = datetime.now()
        start_time = datetime.combine(booking.booking_date, booking.start_time)
        if now < start_time:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Chưa đến thời gian check-in")

        log = CheckinLog(booking_id=booking_id, checkin_time=now)
        db.add(log)
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        room.status = RoomStatus.in_use
        booking.status = BookingStatus.checked_in
        db.commit()
        db.refresh(log)

        event_subject.notify("checked_in", {"room_id": booking.room_id})

        return log

    @staticmethod
    def check_in_via_qr(db: Session, user_id: int, room_code: str):
        room = db.query(Room).filter(Room.room_code == room_code).first()
        if not room:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found.")

        now = datetime.now()
        today = now.date()
        current_time = now.time()
        booking = db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.room_id == room.id,
            Booking.booking_date == today,
            Booking.start_time <= current_time,
            Booking.end_time >= current_time,
            Booking.status == BookingStatus.active
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No matching booking found.")

        log = CheckinLog(booking_id=booking.id, checkin_time=now)
        db.add(log)
        room.status = RoomStatus.in_use
        booking.status = BookingStatus.checked_in
        db.commit()
        db.refresh(log)

        event_subject.notify("checked_in", {"room_id": booking.room_id})

        return log

    @staticmethod
    def check_out(db: Session, user_id: int, booking_id: int):
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
        booking.status = BookingStatus.checked_out
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        room.status = RoomStatus.available
        db.commit()
        db.refresh(log)
        return log
