from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room_schema import RoomReadSchema
from app.services.room_service import RoomService
from typing import List

router = APIRouter(prefix="/admin", tags=["rooms"])

@router.get("/room", response_model=List[RoomReadSchema])
def get_all_rooms(db: Session = Depends(get_db)):
    return RoomService.get_all_rooms(db)
