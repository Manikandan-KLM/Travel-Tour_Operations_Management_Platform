from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.hotel_model import Hotel

from repositories.hotel_repository import (
    hotel_repository
)

from schemas.hotel_schema import HotelCreate


class HotelService:

    def create_hotel(
        self,
        db: Session,
        data: HotelCreate
    ):

        hotel = Hotel(
            hotel_name=data.hotel_name,
            destination_id=data.destination_id,
            address=data.address,
            rating=data.rating,
            contact_number=data.contact_number
        )

        return hotel_repository.create(
            db,
            hotel
        )

    def get_hotels(
        self,
        db: Session
    ):

        return hotel_repository.get_all(db)


hotel_service = HotelService()