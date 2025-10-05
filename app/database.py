# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL  # config.py에서 정의한 URL 불러오기

# 1. DB 연결 엔진 생성
# pool_pre_ping=True: 연결 풀에서 연결을 사용하기 전에 유효성을 확인합니다.
engine = create_engine(
    DATABASE_URL, pool_pre_ping=True
)

# DB 세션 생성 (쿼리 실행에 사용)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의를 위한 기본 클래스
Base = declarative_base()