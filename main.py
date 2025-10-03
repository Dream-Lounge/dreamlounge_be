# main.py (database.py와 config.py 파일을 만들었다고 가정)
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base # Base는 테이블 생성 용도로 사용
from sqlalchemy import text # 이 부분을 추가합니다.
# FastAPI 앱 인스턴스
app = FastAPI()

# ⚠️ 연동 확인용: DB 연결 시도 및 테이블 생성 (선택적)
try:
    # 최초 실행 시 테이블이 없다면 생성
    # Base.metadata.create_all(bind=engine) 
    print("Database connection setup complete.")
except Exception as e:
    print(f"Database connection error: {e}")
    # 실제 운영 환경에서는 앱 시작 실패 처리 필요

# DB 세션을 가져오는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # 세션 사용 후 항상 닫아줍니다.

@app.get("/db-status")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT DATABASE()")).fetchone() 
        connected_db_name = result[0]
        
        # 🚨 수정된 부분: "dl_db" 대신 "dreamlounge_db"로 변경
        if connected_db_name == "dreamlounge_db": 
            return {
                "status": "success",
                "message": "Database connection and authentication successful.",
                "database_name": connected_db_name
            }
        else:
            raise Exception(f"Connected to wrong database: {connected_db_name}")
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed. Check .env and DB user/password: {e}"
        )