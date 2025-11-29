from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, ENVIRONMENT, LOG_LEVEL
from app.models.base import Base

# SQLAlchemy 엔진 생성
# echo=True는 개발 환경에서만 활성화
echo_sql = (ENVIRONMENT == "development" and LOG_LEVEL == "DEBUG")

engine = create_engine(
    DATABASE_URL, 
    echo=echo_sql,  # SQL 쿼리 로그 출력 여부
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,   # 1시간마다 연결 재생성
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 테이블 생성
def create_tables():
    Base.metadata.create_all(bind=engine)


# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()