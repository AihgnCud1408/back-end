from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import time, date
from app.models.room import Room, RoomType
from app.models.booking import Booking, BookingStatus

class RoomService:
    @staticmethod
    def get_all_rooms(db: Session):
        return db.query(Room).all()

    @staticmethod
    def get_available_rooms(db: Session, booking_date: date, start_time: time, end_time: time):
        conflict = db.query(Booking.room_id).filter(
            Booking.booking_date == booking_date,
            Booking.start_time <= end_time,
            Booking.end_time >= start_time,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).subquery()
        available_rooms = db.query(Room).filter(Room.id.notin_(conflict)).all()
        return available_rooms

    @staticmethod
    def create_room(db: Session, room_code: str, room_type: RoomType, location: str):
        existing = db.query(Room).filter(
            Room.room_code == room_code,
        ).first()
        if existing:
            raise HTTPException(status.HTTP_409_CONFLICT, "Room already exists.")

        room = Room(room_code=room_code, room_type=room_type, location=location)
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    @staticmethod
    def delete_room(db: Session, room_id: int):
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found.")

        booking = db.query(Booking).filter(
            Booking.room_id == room.id,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).first()
        if booking:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This room has already been booked.")

        db.delete(room)
        db.commit()
        return None
