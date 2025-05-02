from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room_schema import RoomReadSchema
from app.models.room import Room
from typing import List

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/", response_model=List[RoomReadSchema])
def get_all_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()
    