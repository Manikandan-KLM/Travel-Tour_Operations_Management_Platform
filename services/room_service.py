from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.room_model import Room

from repositories.room_repository import (
    room_repository
)

from repositories.hotel_repository import (
    hotel_repository
)

from schemas.room_schema import RoomCreate


class RoomService:

    def create_room(
        self,
        db: Session,
        data: RoomCreate
    ):

        hotel = hotel_repository.get_by_id(
            db,
            data.hotel_id
        )

        if not hotel:

            raise HTTPException(
                status_code=404,
                detail="Hotel not found"
            )

        room = Room(
            hotel_id=data.hotel_id,
            room_type=data.room_type,
            room_number=data.room_number,
            price_per_night=data.price_per_night,
            capacity=data.capacity,
            availability_status=data.availability_status
        )

        return room_repository.create(
            db,
            room
        )

    def get_hotel_rooms(
        self,
        db: Session,
        hotel_id: int
    ):

        hotel = hotel_repository.get_by_id(
            db,
            hotel_id
        )

        if not hotel:

            raise HTTPException(
                status_code=404,
                detail="Hotel not found"
            )

        return room_repository.get_by_hotel(
            db,
            hotel_id
        )


room_service = RoomService()