from sqlalchemy.orm import Session, selectinload, with_loader_criteria

from src.models.post import Post, Comment
from src.models.club_member import ClubMember
from src.models.user import User
from src.schemas.post import PostCreate, PostUpdate


def _is_president(db: Session, club_id: str, user_id: str) -> bool:
    return db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == user_id,
        ClubMember.role == "president",
        ClubMember.status == "active",
    ).first() is not None


def create_post(db: Session, club_id: str, user: User, data: PostCreate) -> Post:
    is_pres = _is_president(db, club_id, user.id)
    post = Post(
        club_id=club_id,
        author_id=user.id,
        title=data.title,
        content=data.content,
        post_type="notice" if is_pres else "general",
        is_notice=is_pres,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session, club_id: str) -> list[Post]:
    return (
        db.query(Post)
        .options(selectinload(Post.author))
        .filter(Post.club_id == club_id, Post.is_deleted == False)
        .order_by(Post.is_notice.desc(), Post.created_at.desc())
        .all()
    )


def get_post(db: Session, club_id: str, post_id: str) -> Post | None:
    return (
        db.query(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments).selectinload(Comment.author),
            with_loader_criteria(Comment, Comment.is_deleted == False),
        )
        .filter(Post.club_id == club_id, Post.id == post_id, Post.is_deleted == False)
        .first()
    )


def update_post(db: Session, club_id: str, post_id: str, user: User, data: PostUpdate) -> Post:
    post = db.query(Post).filter(
        Post.club_id == club_id, Post.id == post_id, Post.is_deleted == False,
    ).first()
    if not post:
        raise LookupError("게시글을 찾을 수 없습니다.")
    if post.author_id != user.id:
        raise PermissionError("본인 게시글만 수정할 수 있습니다.")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, club_id: str, post_id: str, user: User) -> None:
    post = db.query(Post).filter(
        Post.club_id == club_id, Post.id == post_id, Post.is_deleted == False,
    ).first()
    if not post:
        raise LookupError("게시글을 찾을 수 없습니다.")
    if post.author_id != user.id and not _is_president(db, club_id, user.id):
        raise PermissionError("삭제 권한이 없습니다.")

    post.is_deleted = True
    db.commit()


def toggle_notice(db: Session, club_id: str, post_id: str) -> Post:
    """회장 전용: 게시글 공지 상태 전환."""
    post = db.query(Post).filter(
        Post.club_id == club_id, Post.id == post_id, Post.is_deleted == False,
    ).first()
    if not post:
        raise LookupError("게시글을 찾을 수 없습니다.")

    post.is_notice = not post.is_notice
    post.post_type = "notice" if post.is_notice else "general"
    db.commit()
    db.refresh(post)
    return post


def create_comment(db: Session, post_id: str, user: User, content: str) -> Comment:
    comment = Comment(post_id=post_id, author_id=user.id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, club_id: str, post_id: str, comment_id: str, user: User) -> None:
    comment = db.query(Comment).filter(
        Comment.id == comment_id, Comment.post_id == post_id, Comment.is_deleted == False,
    ).first()
    if not comment:
        raise LookupError("댓글을 찾을 수 없습니다.")
    if comment.author_id != user.id and not _is_president(db, club_id, user.id):
        raise PermissionError("삭제 권한이 없습니다.")

    comment.is_deleted = True
    db.commit()
