# ==========================================================
# 1. 라이브러리 임포트
# ==========================================================
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import SessionLocal, engine, Base
import app.models  # 모델 로드(중요)

# ==========================================================
# 2. FastAPI 인스턴스 생성  ✅ 이 부분이 반드시 먼저 나와야 함!!
# ==========================================================
app = FastAPI()


# ==========================================================
# 3. DB 세션 관리 의존성
# ==========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# 4. (선택) DB 연결 및 테이블 확인용 코드
# ==========================================================
try:
    Base.metadata.create_all(bind=engine)
    print(f"✅ DB 연결 성공: {engine.url.database}")
except Exception as e:
    print(f"❌ DB 연결 실패: {e}")


# ==========================================================
# 5. 여기서부터 API 라우트 작성 가능
# ==========================================================
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to DreamLounge FastAPI Backend."}

# 이후에 /db-status, /db-schema, /db/tables 등의 라우트를 이어 붙이면 됩니다
# from app.database import Base, engine

# print("🧹 Dropping all tables...")
# Base.metadata.drop_all(bind=engine)
# print("✅ Creating new tables...")
# Base.metadata.create_all(bind=engine)
