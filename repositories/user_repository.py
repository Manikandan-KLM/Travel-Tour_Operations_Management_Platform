from sqlalchemy.orm import Session

from models.user_model import User


class UserRepository:

    def get_by_email(
    db: Session,
    email: str
):

        return db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

    def get_by_id(
        self,
        db: Session,
        user_id: int
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create(
        self,
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def update(
        self,
        db: Session,
        user: User
    ):
        db.commit()
        db.refresh(user)

        return user


user_repository = UserRepository()