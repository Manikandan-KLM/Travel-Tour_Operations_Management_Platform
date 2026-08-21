from sqlalchemy.orm import Session
from sqlalchemy import func

from datetime import date
from models.package_model import TourPackage
from models.review_model import Review


class PackageRepository:

    def create(
        self,
        db: Session,
        package: TourPackage
    ):

        db.add(package)
        db.commit()
        db.refresh(package)

        return package

    def get_by_id(
        self,
        db: Session,
        package_id: int
    ):

        return (
            db.query(TourPackage)
            .filter(
                TourPackage.id == package_id
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        package_name: str
    ):

        return (
            db.query(TourPackage)
            .filter(
                TourPackage.package_name == package_name
            )
            .first()
        )

    def update(
        self,
        db: Session,
        package: TourPackage
    ):

        db.commit()
        db.refresh(package)

        return package

    def delete(
        self,
        db: Session,
        package: TourPackage
    ):

        db.delete(package)
        db.commit()

    def get_all(
        self,
        db: Session,
        search: str | None = None,
        status: str | None = None,
        destination_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(TourPackage)

        if search:
            query = query.filter(
                TourPackage.package_name.ilike(
                    f"%{search}%"
                )
            )

        if status:
            query = query.filter(
                TourPackage.status.ilike(status)
            )

        if destination_id:
            query = query.filter(
                TourPackage.destination_id
                == destination_id
            )

        total = query.count()

        offset = (page - 1) * limit

        packages = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return packages, total

def get_package_query(
    db: Session
):

    return db.query(TourPackage)




def search_packages(
    db: Session,
    destination=None,
    min_price=None,
    max_price=None,
    duration=None,
    available=None,
    package_date=None,
    availability=None,
    min_rating=None
):

    query = db.query(TourPackage)

    # Destination
    if destination:

        query = query.filter(
            TourPackage.destination.ilike(
                f"%{destination}%"
            )
        )

    # Minimum price
    if min_price is not None:

        query = query.filter(
            TourPackage.price >= min_price
        )

    # Maximum price
    if max_price is not None:

        query = query.filter(
            TourPackage.price <= max_price
        )

    # Duration
    if duration is not None:

        query = query.filter(
            TourPackage.duration == duration
        )

    # Availability
    if available is not None:

        query = query.filter(
            TourPackage.availability == available
        )

    if package_date:

        query = query.filter(
            TourPackage.start_date == package_date
    )

    # Availability
    if availability is not None:

        query = query.filter(
            TourPackage.availability == availability
        )

    # Rating
    if min_rating is not None:

        query = query.having(
            func.avg(Review.rating) >= min_rating
        )


    return query


package_repository = PackageRepository()