from app.models.base import Base


def get_table_models() -> dict:
    """
    Base를 상속한 모든 모델을 자동으로 딕셔너리로 반환
    
    Returns:
        {table_name: ModelClass} 형태의 딕셔너리
    """
    return {
        mapper.class_.__tablename__: mapper.class_
        for mapper in Base.registry.mappers
    }


def get_model_by_tablename(table_name: str):
    """
    테이블 이름으로 모델 클래스 가져오기
    
    Args:
        table_name: 테이블 이름
    
    Returns:
        해당하는 모델 클래스 또는 None
    """
    models = get_table_models()
    return models.get(table_name)