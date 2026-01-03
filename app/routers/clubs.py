# app/routers/clubs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.club import Club

router = APIRouter(prefix="/clubs", tags=["Clubs"])


@router.get("/")
def get_clubs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """동아리 목록 조회"""
    clubs = db.query(Club).offset(skip).limit(limit).all()
    return clubs


@router.get("/{club_id}")
def get_club(
    club_id: int,
    db: Session = Depends(get_db)
):
    """특정 동아리 조회"""
    club = db.query(Club).filter(Club.club_id == club_id).first()
    
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="동아리를 찾을 수 없습니다"
        )
    
    return club