from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.room import Room
from app.schemas.room_schema import RoomReadSchema

class ManageService:
    def create_room(self, db: Session, room_data: RoomReadSchema):
        existing = db.query(Room).filter(Room.room_code == room_data.room_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Room name already exists")

        room = Room(**room_data.model_dump())
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    def delete_room(self, db: Session, room_id: int):
        room = db.query(Room).filter(Room.room_code == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        db.delete(room)
        db.commit()