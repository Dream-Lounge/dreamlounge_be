# C:\Project\DreamLounge\dream_lounge_be\main.py

# ==========================================================
# 1. 라이브러리 임포트
# ==========================================================
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

from app.database import SessionLocal, engine, Base
import app.models  # 모델 로드(중요)

# ==========================================================
# 2. FastAPI 인스턴스 생성
# ==========================================================
app = FastAPI(title="DreamLounge API")

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
# 4. DB 초기화(선택)
# ==========================================================
try:
    Base.metadata.create_all(bind=engine)
    print(f"✅ DB 연결 성공: {engine.url.database}")
except Exception as e:
    print(f"❌ DB 연결 실패: {e}")

# ==========================================================
# 5. 기본 라우트
# ==========================================================
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to DreamLounge FastAPI Backend."}

# ==========================================================
# 6. 공용 유틸 (테이블 구조/인덱스/DDL 조회)
# ==========================================================
def _table_exists(db: Session, table_name: str) -> bool:
    row = db.execute(
        text("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :t
        """),
        {"t": table_name},
    ).fetchone()
    return (row[0] or 0) > 0

def _describe_table(db: Session, table_name: str) -> List[Dict[str, Any]]:
    if not _table_exists(db, table_name):
        raise HTTPException(status_code=404, detail=f"Table not found: {table_name}")

    rows = db.execute(
        text("""
            SELECT
                COLUMN_NAME,
                COLUMN_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                COLUMN_KEY,
                EXTRA,
                COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :t
            ORDER BY ORDINAL_POSITION
        """),
        {"t": table_name},
    ).mappings().all()
    return [dict(r) for r in rows]

def _table_indexes(db: Session, table_name: str) -> List[Dict[str, Any]]:
    if not _table_exists(db, table_name):
        raise HTTPException(status_code=404, detail=f"Table not found: {table_name}")
    rows = db.execute(text(f"SHOW INDEX FROM `{table_name}`")).mappings().all()
    return [dict(r) for r in rows]

def _table_ddl(db: Session, table_name: str) -> str:
    if not _table_exists(db, table_name):
        raise HTTPException(status_code=404, detail=f"Table not found: {table_name}")
    row = db.execute(text(f"SHOW CREATE TABLE `{table_name}`")).fetchone()
    return row[1] if row and len(row) > 1 else ""

# ==========================================================
# 7. 스키마 라우터 빌더 (테이블별 prefix 생성)
#    /schema/{table}/describe, /indexes, /ddl, /full
# ==========================================================
def build_schema_router(table_name: str) -> APIRouter:
    router = APIRouter(prefix=f"/schema/{table_name}", tags=[f"Schema:{table_name}"])

    @router.get("/describe")
    def describe(db: Session = Depends(get_db)):
        return {
            "status": "success",
            "table": table_name,
            "columns": _describe_table(db, table_name),
        }

    @router.get("/indexes")
    def indexes(db: Session = Depends(get_db)):
        return {
            "status": "success",
            "table": table_name,
            "indexes": _table_indexes(db, table_name),
        }

    @router.get("/ddl")
    def ddl(db: Session = Depends(get_db)):
        return {
            "status": "success",
            "table": table_name,
            "ddl": _table_ddl(db, table_name),
        }

    @router.get("/full")
    def full(db: Session = Depends(get_db)):
        return {
            "status": "success",
            "table": table_name,
            "describe": _describe_table(db, table_name),
            "indexes": _table_indexes(db, table_name),
            "ddl": _table_ddl(db, table_name),
        }

    return router

# ==========================================================
# 8. 전체 테이블 목록/ORM 비교 라우트 + include_router
# ==========================================================
@app.get("/schema/tables", tags=["Schema:tables"])
def list_tables(db: Session = Depends(get_db)):
    # 실제 DB 테이블 목록
    db_tables = [
        r[0]
        for r in db.execute(
            text("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
            """)
        ).fetchall()
    ]

    # ORM 인식 테이블
    orm_tables = sorted(list(Base.metadata.tables.keys()))
    return {
        "status": "success",
        "database_name": engine.url.database,
        "db_tables": db_tables,
        "orm_tables": orm_tables,
        "diff": {
            "in_db_not_in_orm": sorted([t for t in db_tables if t not in orm_tables]),
            "in_orm_not_in_db": sorted([t for t in orm_tables if t not in db_tables]),
        },
    }

# 스키마 라우터 등록 (요청하신 테이블들)
TABLE_NAMES = [
    "clubs",
    "users",
    "user_members",
    "user_guests",
    "user_admins",
    "submitted",
    "temp_saved",
]

for t in TABLE_NAMES:
    app.include_router(build_schema_router(t))

# ==========================================================
# 9. FastAPI 문서 (자동)
#    /docs 에서 각 테이블 라우트 실행 가능
# ==========================================================
# (별도 코드 필요 없음)
