from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from models.customer_model import Customer

from repositories.customer_repository import (
    customer_repository
)

from schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate
)


class CustomerService:

    def create_customer(
        self,
        db: Session,
        data: CustomerCreate
    ):

        # Check duplicate email
        existing = (
            customer_repository.get_by_email(
                db,
                data.email
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer email already exists"
            )

        customer = Customer(
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
            emergency_contact=data.emergency_contact
        )

        return customer_repository.create(
            db,
            customer
        )

    def get_customers(
        self,
        db: Session
    ):

        return customer_repository.get_all(db)

    def get_customer(
        self,
        db: Session,
        customer_id: int
    ):

        customer = customer_repository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return customer

    def update_customer(
        self,
        db: Session,
        customer_id: int,
        data: CustomerUpdate
    ):

        customer = self.get_customer(
            db,
            customer_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Check email uniqueness
        if "email" in update_data:

            existing = (
                customer_repository.get_by_email(
                    db,
                    update_data["email"]
                )
            )

            if existing and existing.id != customer.id:

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Customer email already exists"
                )

        for field, value in update_data.items():

            setattr(
                customer,
                field,
                value
            )

        return customer_repository.update(
            db,
            customer
        )


def search_customers(
    db: Session,
    name=None,
    email=None,
    phone=None,
    page=1,
    limit=10,
    sort_by="id",
    sort_order="asc"
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

    query = customer_repository.search_customers(
        db=db,
        name=name,
        email=email,
        phone=phone
    )

    allowed_sort_fields = {
        "id": "id",
        "name": "name",
        "email": "email"
    }

    if sort_by not in allowed_sort_fields:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if sort_order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    column = getattr(
        Customer,
        allowed_sort_fields[sort_by]
    )

    if sort_order == "desc":

        query = query.order_by(
            column.desc()
        )

    else:

        query = query.order_by(
            column.asc()
        )

    total = query.count()

    offset = (page - 1) * limit

    customers = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (
        (total + limit - 1) // limit
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": customers
    }

