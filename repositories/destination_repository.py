from sqlalchemy.orm import Session

from models.destination_model import Destination


class DestinationRepository:

    def create(
        self,
        db: Session,
        destination: Destination
    ):
        db.add(destination)

        db.commit()

        db.refresh(destination)

        return destination

    def get_by_id(
        self,
        db: Session,
        destination_id: int
    ):
        return (
            db.query(Destination)
            .filter(
                Destination.id == destination_id
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        name: str
    ):
        return (
            db.query(Destination)
            .filter(
                Destination.name == name
            )
            .first()
        )

    def update(
        self,
        db: Session,
        destination: Destination
    ):
        db.commit()

        db.refresh(destination)

        return destination

    def delete(
        self,
        db: Session,
        destination: Destination
    ):
        db.delete(destination)

        db.commit()

    def get_all(
        self,
        db: Session,
        search: str | None = None,
        country: str | None = None,
        season: str | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Destination)

        # Search by destination name
        if search:
            query = query.filter(
                Destination.name.ilike(
                    f"%{search}%"
                )
            )

        # Filter by country
        if country:
            query = query.filter(
                Destination.country.ilike(country)
            )

        # Filter by season
        if season:
            query = query.filter(
                Destination.best_season.ilike(season)
            )

        # Total count before pagination
        total = query.count()

        # Pagination
        offset = (page - 1) * limit

        destinations = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return destinations, total


destination_repository = DestinationRepository()