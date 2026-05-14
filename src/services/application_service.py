from datetime import datetime
from sqlalchemy.orm import Session, selectinload

from src.models.application import Application, ApplicationAnswer, ApplicationForm
from src.models.club import Club
from src.models.club_member import ClubMember
from src.models.user import User
from src.schemas.application import ApplicationCreate, ApplicationUpdate


def _validate_required_answers(form_questions, answers) -> None:
    """제출 시 필수 질문이 모두 답변됐는지 확인."""
    answered_ids = {a.question_id for a in answers}
    for q in form_questions:
        if q.is_required and q.id not in answered_ids:
            raise ValueError(f"필수 항목에 답변이 누락되었습니다: {q.question_text}")


def create_application(db: Session, user: User, data: ApplicationCreate) -> Application:
    form = db.get(ApplicationForm, data.form_id)
    if not form or not form.is_active:
        raise ValueError("존재하지 않거나 비활성화된 신청 폼입니다.")

    existing_submitted = (
        db.query(Application)
        .filter(
            Application.form_id == data.form_id,
            Application.user_id == user.id,
            Application.is_draft == False,
        )
        .first()
    )
    if existing_submitted:
        raise ValueError("이미 제출한 신청서가 있습니다.")

    if not data.is_draft:
        _validate_required_answers(form.questions, data.answers)

    now = datetime.utcnow()
    app = Application(
        form_id=data.form_id,
        user_id=user.id,
        is_draft=data.is_draft,
        status="draft" if data.is_draft else "submitted",
        submitted_at=None if data.is_draft else now,
    )
    db.add(app)
    db.flush()

    for ans in data.answers:
        db.add(ApplicationAnswer(
            application_id=app.id,
            question_id=ans.question_id,
            answer_text=ans.answer_text,
        ))

    db.commit()
    return (
        db.query(Application)
        .options(selectinload(Application.answers))
        .filter(Application.id == app.id)
        .first()
    )


def update_application(
    db: Session, user: User, application_id: str, data: ApplicationUpdate
) -> Application:
    app = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user.id)
        .first()
    )
    if not app:
        raise LookupError("신청서를 찾을 수 없습니다.")
    if not app.is_draft:
        raise ValueError("이미 제출된 신청서는 수정할 수 없습니다.")

    submitting = data.is_draft is False

    if data.answers is not None:
        for ans in list(app.answers):
            db.delete(ans)
        db.flush()
        for ans in data.answers:
            db.add(ApplicationAnswer(
                application_id=app.id,
                question_id=ans.question_id,
                answer_text=ans.answer_text,
            ))
        app.updated_at = datetime.utcnow()
        db.flush()
        db.refresh(app)

    if submitting:
        answers_to_check = data.answers if data.answers is not None else app.answers
        form = db.get(ApplicationForm, app.form_id)
        _validate_required_answers(form.questions, answers_to_check)
        app.is_draft = False
        app.status = "submitted"
        app.submitted_at = datetime.utcnow()

    db.commit()
    return (
        db.query(Application)
        .options(selectinload(Application.answers))
        .filter(Application.id == app.id)
        .first()
    )


def get_draft_applications(db: Session, user: User) -> list[Application]:
    return (
        db.query(Application)
        .filter(Application.user_id == user.id, Application.is_draft == True)
        .order_by(Application.updated_at.desc())
        .all()
    )


def get_draft_application(db: Session, user: User, application_id: str) -> Application | None:
    return (
        db.query(Application)
        .options(selectinload(Application.answers))
        .filter(
            Application.id == application_id,
            Application.user_id == user.id,
            Application.is_draft == True,
        )
        .first()
    )


def get_submitted_applications(db: Session, user: User) -> list[Application]:
    return (
        db.query(Application)
        .filter(Application.user_id == user.id, Application.is_draft == False)
        .order_by(Application.submitted_at.desc())
        .all()
    )


def get_submitted_application(db: Session, user: User, application_id: str) -> Application | None:
    return (
        db.query(Application)
        .options(selectinload(Application.answers))
        .filter(
            Application.id == application_id,
            Application.user_id == user.id,
            Application.is_draft == False,
        )
        .first()
    )


def get_active_clubs(db: Session, user: User) -> list[dict]:
    memberships = (
        db.query(ClubMember)
        .join(Club, ClubMember.club_id == Club.id)
        .filter(ClubMember.user_id == user.id, ClubMember.status == "active")
        .all()
    )
    return [
        {
            "club_id": m.club_id,
            "club_name": m.club.name,
            "role": m.role,
            "joined_at": m.joined_at,
        }
        for m in memberships
    ]
