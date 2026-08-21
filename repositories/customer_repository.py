from sqlalchemy.orm import Session

from models.customer_model import Customer


class CustomerRepository:

    def create(
        self,
        db: Session,
        customer: Customer
    ):

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    def get_by_id(
        self,
        db: Session,
        customer_id: int
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.id == customer_id
            )
            .first()
        )

    def get_by_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.email == email
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(Customer)
            .order_by(Customer.id.desc())
            .all()
        )

    def update(
        self,
        db: Session,
        customer: Customer
    ):

        db.commit()
        db.refresh(customer)

        return customer


def search_customers(
    db: Session,
    name=None,
    email=None,
    phone=None
):

    query = db.query(Customer)

    # Name
    if name:

        query = query.filter(
            Customer.name.ilike(
                f"%{name}%"
            )
        )

    # Email
    if email:

        query = query.filter(
            Customer.email.ilike(
                f"%{email}%"
            )
        )

    # Phone
    if phone:

        query = query.filter(
            Customer.phone.ilike(
                f"%{phone}%"
            )
        )

    return query


customer_repository = CustomerRepository()