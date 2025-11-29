from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect

# 로깅 초기화 (가장 먼저)
from app.core.logging_config import setup_logging, get_logger
from app.config import LOG_LEVEL, ENVIRONMENT, log_database_config

setup_logging(log_level=LOG_LEVEL)
logger = get_logger(__name__)

# 데이터베이스 설정 로깅
log_database_config()

# 나머지 import
from app.database import engine, SessionLocal, get_db
from app.models.base import Base
from app.utils.models import get_table_models, get_model_by_tablename
from app.routers import members

app = FastAPI(
    title="Club Management System",
    description="동아리 관리 시스템 API",
    version="1.0.0"
)

app.include_router(members.router)


@app.on_event("startup")
def on_startup():
    logger.info("Application startup initiated")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # 등록된 모델 확인 (DEBUG 레벨에서만)
        models = get_table_models()
        logger.debug(f"Registered models: {list(models.keys())}")
        
        logger.info("Application startup completed")
    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Application shutdown initiated")


# ... 나머지 코드는 동일


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Application shutdown initiated")


@app.get("/")
def read_root():
    logger.debug("Root endpoint accessed")
    return {
        "message": "Club Management API",
        "environment": ENVIRONMENT,
        "endpoints": {
            "database_info": "/db/info",
            "all_tables": "/db/tables",
            "table_structure": "/db/tables/{table_name}",
            "table_data_sample": "/db/tables/{table_name}/data"
        }
    }


# ... 나머지 엔드포인트는 동일

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
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
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
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    # ✅ 동적으로 모델 가져오기
    model = get_model_by_tablename(table_name)
    
    if not model:
        raise HTTPException(
            status_code=500, 
            detail=f"Model for table '{table_name}' not found"
        )
    
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
    # ✅ 동적으로 모델 가져오기
    model = get_model_by_tablename(table_name)
    
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Model for table '{table_name}' not found"
        )
    
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


@app.get("/db/models")
def get_registered_models():
    """등록된 모든 모델 정보"""
    models = get_table_models()
    
    return {
        "total_models": len(models),
        "models": {
            table_name: {
                "class_name": model.__name__,
                "module": model.__module__,
                "table_name": table_name
            }
            for table_name, model in models.items()
        }
    }