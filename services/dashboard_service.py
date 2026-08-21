from sqlalchemy.orm import Session

from repositories import dashboard_repository


def get_dashboard(
    db: Session
):

    return (
        dashboard_repository
        .get_dashboard_data(db)
    )