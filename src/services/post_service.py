from sqlalchemy.orm import Session


def create_post(db: Session, user_id: str, club_id: str, data: dict):
    """게시글 생성. 회장이 작성하면 자동으로 is_notice=True."""
    raise NotImplementedError


def delete_post(db: Session, user_id: str, post_id: str) -> None:
    """게시글 소프트 삭제. 회장은 모든 글, 부원은 본인 글만 삭제 가능."""
    raise NotImplementedError
