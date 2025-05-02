from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.room_schema import RoomReadSchema
from app.db.session import get_db
from app.services.manage_room_service import ManageService
from app.models.room import Room

router = APIRouter(prefix="/manage", tags=["manage"])

@router.get("/rooms")
def get_all_rooms(db: Session= Depends(get_db)):
        return db.query(Room).all()

@router.post("/rooms/create", response_model=RoomReadSchema)
def create_room_api(room: RoomReadSchema, db: Session = Depends(get_db)):
    return ManageService().create_room(db, room)

@router.delete("/rooms/{room_id}")
def delete_room_api(room_id: int, db: Session = Depends(get_db)):
    return ManageService().delete_room(db, room_id)