# migrate_test_application.py
from sqlalchemy import text
from app.database import engine
from app.models.base import Base
from app.models.test_application import TestApplication

def migrate():
    print("[MIGRATION] Migrating test_applications table...")
    
    try:
        with engine.connect() as conn:
            # 1. 기존 테이블 삭제
            print("[MIGRATION] Dropping existing test_applications table...")
            conn.execute(text("DROP TABLE IF EXISTS test_applications"))
            conn.commit()
            print("[MIGRATION] ✓ Table dropped")
        
        # 2. 새 스키마로 테이블 생성
        print("[MIGRATION] Creating test_applications table with new schema...")
        Base.metadata.create_all(bind=engine, tables=[TestApplication.__table__])
        print("[MIGRATION] ✓ Table created")
        
        print("[MIGRATION] ✅ Migration completed successfully!")
        print("[MIGRATION] student_id is now the PRIMARY KEY")
        
    except Exception as e:
        print(f"[MIGRATION] ❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()