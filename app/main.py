from fastapi import FastAPI, Depends, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from pathlib import Path
from contextlib import asynccontextmanager
from app.routers import members, applications, debug
from app.config import ENVIRONMENT, LOG_LEVEL
from app.utils.models import get_model_by_tablename
from app.core.logging_config import setup_logging, get_logger

from app.database import engine, SessionLocal, get_db
from app.models.base import Base
from app.models import (
    Member, Club, ClubManager, Application, ClubMembership, TestApplication,
)

# ✅ 로거 초기화
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 로깅 설정 초기화
    setup_logging(log_level=LOG_LEVEL)
    
    # [Startup 로직]
    logger.info("[STARTUP] Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("[STARTUP] Database tables created successfully!")
    except Exception as e:
        logger.error(f"[STARTUP ERROR] {e}", exc_info=True)
    
    yield  # 👈 앱이 실행되는 동안 대기 (이 지점에서 API 통신이 이루어짐)
    
    # [Shutdown 로직] - 필요 시 작성 (예: DB 연결 해제 등)
    logger.info("[SHUTDOWN] Application is shutting down...")

app = FastAPI(
    title="Club Management System",
    description="동아리 관리 시스템 API",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ 정적 파일 디렉토리 마운트 (form 폴더) - 개발 환경에서만
FORM_DIR = Path(__file__).parent.parent / "form"
if ENVIRONMENT == 'development' and FORM_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FORM_DIR)), name="static")


@app.get("/")
def read_root():
    """API 루트 엔드포인트"""
    endpoints = {
        "docs": "/docs",
        "members": "/members",
        "applications": "/applications"
    }
    
    # 개발 환경에서만 디버그 엔드포인트 표시
    if ENVIRONMENT == 'development':
        endpoints.update({
            "database_info": "/db/info",
            "all_tables": "/db/tables",
            "table_structure": "/db/tables/{table_name}",
            "table_data_sample": "/db/tables/{table_name}/data",
            "test_form": "/form"
        })
    
    return {
        "message": "Club Management API",
        "environment": ENVIRONMENT,
        "endpoints": endpoints
    }


# ========================================
# 🔧 개발 환경 전용 엔드포인트
# ========================================
if ENVIRONMENT == 'development':
    
    @app.get("/form", response_class=HTMLResponse)
    def show_form():
        """테스트 신청 폼 HTML 반환"""
        form_file = FORM_DIR / "index.html"
        if not form_file.exists():
            return HTMLResponse(
                content="<h1>폼 파일을 찾을 수 없습니다.</h1>",
                status_code=404
            )
        return FileResponse(form_file)

    
    @app.get("/db/info")
    def get_database_info():
        """데이터베이스 기본 정보"""
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "database": engine.url.database,
            "host": engine.url.host,
            "port": engine.url.port,
            "driver": engine.url.drivername,
            "total_tables": len(tables),
            "tables": tables
        }

    
    @app.get("/db/tables")
    def get_all_tables_structure():
        """모든 테이블의 구조 정보"""
        inspector = inspect(engine)
        tables_info = {}
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            pk_constraint = inspector.get_pk_constraint(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            indexes = inspector.get_indexes(table_name)
            
            tables_info[table_name] = {
                "columns": [
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col["nullable"],
                        "default": str(col["default"]) if col["default"] else None,
                        "comment": col.get("comment", "")
                    }
                    for col in columns
                ],
                "primary_key": pk_constraint.get("constrained_columns", []),
                "foreign_keys": [
                    {
                        "column": fk["constrained_columns"],
                        "refers_to": f"{fk['referred_table']}.{fk['referred_columns']}"
                    }
                    for fk in foreign_keys
                ],
                "indexes": [
                    {
                        "name": idx["name"],
                        "columns": idx["column_names"],
                        "unique": idx["unique"]
                    }
                    for idx in indexes
                ]
            }
        
        return tables_info

    
    @app.get("/db/tables/{table_name}")
    def get_table_structure(table_name: str):
        """특정 테이블의 상세 구조"""
        inspector = inspect(engine)
        
        if table_name not in inspector.get_table_names():
            return {"error": f"Table '{table_name}' not found"}
        
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        unique_constraints = inspector.get_unique_constraints(table_name)
        check_constraints = inspector.get_check_constraints(table_name)
        
        return {
            "table_name": table_name,
            "columns": [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col["nullable"],
                    "default": str(col["default"]) if col["default"] else None,
                    "autoincrement": col.get("autoincrement", False),
                    "comment": col.get("comment", "")
                }
                for col in columns
            ],
            "primary_key": {
                "name": pk_constraint.get("name"),
                "columns": pk_constraint.get("constrained_columns", [])
            },
            "foreign_keys": [
                {
                    "name": fk.get("name"),
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"],
                    "onupdate": fk.get("onupdate"),
                    "ondelete": fk.get("ondelete")
                }
                for fk in foreign_keys
            ],
            "indexes": [
                {
                    "name": idx["name"],
                    "columns": idx["column_names"],
                    "unique": idx["unique"]
                }
                for idx in indexes
            ],
            "unique_constraints": [
                {
                    "name": uc.get("name"),
                    "columns": uc["column_names"]
                }
                for uc in unique_constraints
            ],
            "check_constraints": [
                {
                    "name": cc.get("name"),
                    "sqltext": str(cc.get("sqltext", ""))
                }
                for cc in check_constraints
            ]
        }

    
    @app.get("/db/tables/{table_name}/data")
    def get_table_data_sample(
        table_name: str, 
        limit: int = 10,
        db: Session = Depends(get_db)
    ):
        """특정 테이블의 데이터 샘플 조회"""
        inspector = inspect(engine)
        
        if table_name not in inspector.get_table_names():
            return {"error": f"Table '{table_name}' not found"}
        
        # ✅ 동적으로 모델 가져오기 (utils 함수 사용)
        model = get_model_by_tablename(table_name)
        if not model:
            return {"error": f"Model for table '{table_name}' not configured"}
        
        # 데이터 조회
        data = db.query(model).limit(limit).all()
        
        # 컬럼 정보
        columns = inspector.get_columns(table_name)
        column_names = [col["name"] for col in columns]
        
        # 데이터 변환
        result = []
        for row in data:
            row_dict = {}
            for col_name in column_names:
                value = getattr(row, col_name, None)
                # datetime 객체를 문자열로 변환
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                # Enum 객체를 문자열로 변환
                elif hasattr(value, 'value'):
                    value = value.value
                row_dict[col_name] = value
            result.append(row_dict)
        
        return {
            "table_name": table_name,
            "total_rows_in_sample": len(result),
            "columns": column_names,
            "data": result
        }

    
    @app.get("/db/tables/{table_name}/count")
    def get_table_row_count(table_name: str, db: Session = Depends(get_db)):
        """특정 테이블의 전체 레코드 수"""
        # ✅ 동적으로 모델 가져오기 (utils 함수 사용)
        model = get_model_by_tablename(table_name)
        if not model:
            return {"error": f"Model for table '{table_name}' not configured"}
        
        count = db.query(model).count()
        
        return {
            "table_name": table_name,
            "total_rows": count
        }

    
    @app.get("/db/relationships")
    def get_table_relationships():
        """모든 테이블 간의 관계 정보"""
        inspector = inspect(engine)
        relationships = {}
        
        for table_name in inspector.get_table_names():
            foreign_keys = inspector.get_foreign_keys(table_name)
            
            if foreign_keys:
                relationships[table_name] = [
                    {
                        "from_column": fk["constrained_columns"],
                        "to_table": fk["referred_table"],
                        "to_column": fk["referred_columns"],
                        "constraint_name": fk.get("name")
                    }
                    for fk in foreign_keys
                ]
        
        return relationships

    
    @app.get("/db/schema/mermaid")
    def get_mermaid_erd():
        """Mermaid ERD 다이어그램 생성"""
        inspector = inspect(engine)
        mermaid_lines = ["erDiagram"]
        
        # 각 테이블의 컬럼 정의
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            pk_constraint = inspector.get_pk_constraint(table_name)
            pk_columns = pk_constraint.get("constrained_columns", [])
            
            mermaid_lines.append(f"    {table_name.upper()} {{")
            
            for col in columns:
                col_type = str(col["type"]).split("(")[0]
                is_pk = "PK" if col["name"] in pk_columns else ""
                comment = col.get("comment", col["name"])
                mermaid_lines.append(f'        {col_type} {col["name"]} {is_pk} "{comment}"')
            
            mermaid_lines.append("    }")
        
        # 관계 정의
        for table_name in inspector.get_table_names():
            foreign_keys = inspector.get_foreign_keys(table_name)
            
            for fk in foreign_keys:
                from_table = table_name.upper()
                to_table = fk["referred_table"].upper()
                mermaid_lines.append(f"    {to_table} ||--o{{ {from_table} : has")
        
        return {
            "mermaid_code": "\n".join(mermaid_lines)
        }

    
    @app.post("/test/apply")
    def submit_test_application(
        student_id: str = Form(...),
        department: str = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        db: Session = Depends(get_db),
    ):
        """테스트 신청서 저장 - JSON 응답"""
        
        # ✅ 중복 학번 체크
        existing = db.query(TestApplication).filter(
            TestApplication.student_id == student_id
        ).first()
        
        if existing:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "duplicate",
                    "message": f"이미 존재하는 학번입니다: {student_id}"
                }
            )
        
        # DB에 저장
        try:
            app_row = TestApplication(
                student_id=student_id,
                department=department,
                name=name,
                email=email,
                phone=phone,
            )
            db.add(app_row)
            db.commit()
            db.refresh(app_row)
            
            return JSONResponse(
                status_code=201,
                content={
                    "success": True,
                    "message": "테스트 신청이 완료되었습니다",
                    "data": {
                        "student_id": app_row.student_id,
                        "department": app_row.department,
                        "name": app_row.name,
                        "email": app_row.email,
                        "phone": app_row.phone,
                        "created_at": app_row.created_at.isoformat() if app_row.created_at else None
                    }
                }
            )
        except Exception as e:
            db.rollback()
            logger.error(f"테스트 신청 저장 실패: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "server_error",
                    "message": "신청 처리 중 오류가 발생했습니다"
                }
            )


# ========================================
# 🔌 라우터 등록
# ========================================
app.include_router(members.router)
app.include_router(applications.router)

# 디버그 라우터는 개발 환경에서만 등록
if ENVIRONMENT == 'development':
    app.include_router(debug.router)