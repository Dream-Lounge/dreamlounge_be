# C:\Project\DreamLounge\dream_lounge_be\main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text 

# app 패키지 내의 DB 및 모델들을 임포트합니다.
from app.database import SessionLocal, engine, Base # Base를 직접 사용합니다.
from app import models # 모델 파일을 로드하여 Base.metadata가 테이블을 인식하게 합니다.

app = FastAPI()

# ---------------------------------------------------
# 1. 애플리케이션 시작 시 테이블 생성 확인 로직
# ---------------------------------------------------
try:
    # Base에 정의된 모든 모델(User, UserMember 등)을 추적합니다.
    all_table_names = list(Base.metadata.tables.keys())
    
    # DB에 테이블이 없으면 생성합니다. (이미 존재하면 아무것도 하지 않음)
    Base.metadata.create_all(bind=engine)
    
    print("--- Database Table Status ---")
    print(f"✅ Connection successful to: {engine.url.database}")
    print(f"✅ Total models found and checked: {len(all_table_names)}")
    print(f"✅ Tables checked/created: {', '.join(all_table_names)}")
    print("-----------------------------")

except Exception as e:
    print("--- ❌ CRITICAL DATABASE ERROR ---")
    print(f"❌ Database connection or Table creation failed: {e}")
    print("❌ Check DB server status and connection parameters in .env file.")
    print("-----------------------------------")


# ---------------------------------------------------
# 2. DB 세션 관리 의존성 주입 함수
# ---------------------------------------------------
# 각 API 요청마다 DB 세션을 생성하고 요청 완료 후 닫아줍니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# ---------------------------------------------------
# 3. API 엔드포인트 정의
# ---------------------------------------------------

@app.get("/", tags=["Root"])
def read_root():
    """기본 경로 (404 방지용)"""
    return {"message": "Welcome to DreamLounge FastAPI Backend. Check /db-schema for DB details."}


@app.get("/db-status", tags=["Database"])
def check_db_connection(db: Session = Depends(get_db)):
    """DB 연결 및 인증 상태 확인"""
    try:
        # DB 이름 확인 쿼리 실행
        result = db.execute(text("SELECT DATABASE()")).fetchone() 
        connected_db_name = result[0]
        
        # 실제 연결된 DB 이름과 .env의 DB_NAME 값이 일치하는지 확인
        if connected_db_name == "dreamlounge_db": 
            return {
                "status": "success",
                "message": "Database connection and authentication successful.",
                "database_name": connected_db_name
            }
        else:
            # 이 에러가 발생하면 .env 파일의 DB_NAME을 확인해야 합니다.
            raise HTTPException(
                status_code=500,
                detail=f"Connected to wrong database: {connected_db_name}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed. Check .env and DB user/password: {e}"
        )


@app.get("/db-schema", tags=["Database"])
def get_db_schema_details(db: Session = Depends(get_db)):
    """현재 ORM 모델에 정의된 모든 테이블의 스키마 정보를 반환합니다."""
    try:
        schema_details = {}
        
        for table_name, table_obj in Base.metadata.tables.items():
            columns = []
            
            for col in table_obj.columns:
                col_type = str(col.type)
                
                fk_info = None
                if col.foreign_keys:
                    fk = list(col.foreign_keys)[0]
                    fk_info = f"FK -> {fk.column.table.name}.{fk.column.name}"
                
                columns.append({
                    "name": col.name,
                    "type": col_type,
                    "primary_key": col.primary_key,
                    "unique": col.unique,
                    "nullable": col.nullable,
                    "default": col.default.arg if col.default else None,
                    "foreign_key": fk_info
                })
            
            schema_details[table_name] = columns
            
        return {
            "status": "success",
            "database_name": engine.url.database,
            "total_tables": len(schema_details),
            "tables": schema_details
        }
    
    except Exception as e:
        # 이 에러는 DB 연결이 끊어졌거나 세션 문제가 있을 때 발생할 수 있습니다.
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch schema details: {e}"
        )