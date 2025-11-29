"""
Club 테이블의 'type' 컬럼을 'club_type'으로 변경하기 위한 마이그레이션 스크립트
개발 초기 단계용 (데이터가 없는 경우)

사용법:
  uv run python migrate_club_type.py
"""

from app.database import engine
from app.models.base import Base
# ✅ 모든 모델 import (Foreign Key 관계 때문에 필요)
from app.models import (
    Member, Club, ClubManager, Application, ClubMembership
)

def migrate():
    print("[MIGRATION] Starting migration: 'type' → 'club_type'")
    print("[MIGRATION] ⚠️  This will drop and recreate ALL tables")
    
    try:
        # 1. 모든 테이블 삭제 (FK 제약 조건 때문에 필요)
        print("[MIGRATION] Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("[MIGRATION] ✓ All tables dropped")
        
        # 2. 모든 테이블 재생성 (새 스키마로)
        print("[MIGRATION] Creating all tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("[MIGRATION] ✓ All tables created")
        
        print("[MIGRATION] ✅ Migration completed successfully!")
        print("[MIGRATION] Column 'type' has been renamed to 'club_type'")
        
    except Exception as e:
        print(f"[MIGRATION] ❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()