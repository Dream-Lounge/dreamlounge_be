from sqlalchemy.orm import Session
from src.models.club import Club
from src.models.application import ApplicationForm


def get_club(db: Session, club_id: str) -> Club | None:
    return db.get(Club, club_id)


def get_active_form(db: Session, club_id: str) -> ApplicationForm | None:
    return (
        db.query(ApplicationForm)
        .filter(ApplicationForm.club_id == club_id, ApplicationForm.is_active == True)
        .first()
    )
