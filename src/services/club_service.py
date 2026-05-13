from sqlalchemy.orm import Session
from src.models.club import Club
from src.models.application import ApplicationForm


def get_club(db: Session, club_id: str) -> Club | None:
    """club_id로 동아리 상세 정보 조회 (tags 포함)."""
    raise NotImplementedError


def get_active_form(db: Session, club_id: str) -> ApplicationForm | None:
    """동아리의 활성 신청 폼과 질문 목록 조회 (is_active=True인 최신 폼)."""
    raise NotImplementedError
