from sqlalchemy.orm import Session

from models.room_model import Room


class RoomRepository:

    def create(
        self,
        db: Session,
        room: Room
    ):

        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    def get_by_id(
        self,
        db: Session,
        room_id: int
    ):

        return (
            db.query(Room)
            .filter(
                Room.id == room_id
            )
            .first()
        )

    def get_by_hotel(
        self,
        db: Session,
        hotel_id: int
    ):

        return (
            db.query(Room)
            .filter(
                Room.hotel_id == hotel_id
            )
            .all()
        )


room_repository = RoomRepository()