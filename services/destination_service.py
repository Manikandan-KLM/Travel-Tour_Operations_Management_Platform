from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.destination_model import Destination
from repositories.destination_repository import (
    destination_repository
)
from schemas.destination_schema import (
    DestinationCreate,
    DestinationUpdate
)


class DestinationService:

    def create_destination(
        self,
        db: Session,
        data: DestinationCreate
    ):

        existing = destination_repository.get_by_name(
            db,
            data.name
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Destination already exists"
            )

        if data.status not in [
            "Active",
            "Inactive"
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be Active or Inactive"
            )

        destination = Destination(
            name=data.name,
            country=data.country,
            state=data.state,
            description=data.description,
            best_season=data.best_season,
            status=data.status
        )

        return destination_repository.create(
            db,
            destination
        )

    def get_destination(
        self,
        db: Session,
        destination_id: int
    ):

        destination = destination_repository.get_by_id(
            db,
            destination_id
        )

        if not destination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination not found"
            )

        return destination

    def get_destinations(
        self,
        db: Session,
        search: str | None,
        country: str | None,
        season: str | None,
        page: int,
        limit: int
    ):

        if page < 1:
            raise HTTPException(
                status_code=400,
                detail="Page must be greater than 0"
            )

        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limit must be between 1 and 100"
            )

        return destination_repository.get_all(
            db=db,
            search=search,
            country=country,
            season=season,
            page=page,
            limit=limit
        )

    def update_destination(
        self,
        db: Session,
        destination_id: int,
        data: DestinationUpdate
    ):

        destination = self.get_destination(
            db,
            destination_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "status" in update_data:

            if update_data["status"] not in [
                "Active",
                "Inactive"
            ]:
                raise HTTPException(
                    status_code=400,
                    detail="Status must be Active or Inactive"
                )

        if "name" in update_data:

            existing = destination_repository.get_by_name(
                db,
                update_data["name"]
            )

            if (
                existing
                and existing.id != destination.id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="Destination name already exists"
                )

        for field, value in update_data.items():
            setattr(
                destination,
                field,
                value
            )

        return destination_repository.update(
            db,
            destination
        )

    def delete_destination(
        self,
        db: Session,
        destination_id: int
    ):

        destination = self.get_destination(
            db,
            destination_id
        )

        destination_repository.delete(
            db,
            destination
        )

        return {
            "message": "Destination deleted successfully"
        }


destination_service = DestinationService()