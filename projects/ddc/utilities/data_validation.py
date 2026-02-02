"""
데이터 검증 & 변환 - 입력 무결성 보장

역할:
- 스키마 검증
- 타입 변환
- 데이터 정제
- 에러 보고
"""

from typing import Dict, Any, List, Type, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    """데이터 타입"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@dataclass
class FieldSchema:
    """필드 스키마"""
    name: str
    data_type: DataType
    required: bool = True
    min_length: int = None
    max_length: int = None
    min_value: float = None
    max_value: float = None
    pattern: str = None
    allowed_values: List[Any] = None
    default_value: Any = None


class SchemaValidator:
    """스키마 검증기"""
    
    def __init__(self):
        self.schemas: Dict[str, List[FieldSchema]] = {}
        self.validation_errors = []
    
    def register_schema(self, name: str, fields: List[FieldSchema]):
        """스키마 등록"""
        self.schemas[name] = fields
    
    def validate(self, schema_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 검증"""
        
        self.validation_errors = []
        
        if schema_name not in self.schemas:
            return {'valid': False, 'error': f'Schema {schema_name} not found'}
        
        schema_fields = self.schemas[schema_name]
        validated_data = {}
        
        # 필드별 검증
        for field in schema_fields:
            value = data.get(field.name)
            
            # 필수 필드 확인
            if value is None:
                if field.required:
                    if field.default_value is not None:
                        value = field.default_value
                    else:
                        self.validation_errors.append(f"Field '{field.name}' is required")
                        continue
                else:
                    continue
            
            # 타입 검증 & 변환
            try:
                converted_value = self._convert_and_validate(value, field)
                validated_data[field.name] = converted_value
            except ValueError as e:
                self.validation_errors.append(str(e))
        
        if self.validation_errors:
            return {
                'valid': False,
                'errors': self.validation_errors,
                'data': None
            }
        
        return {
            'valid': True,
            'errors': [],
            'data': validated_data
        }
    
    def _convert_and_validate(self, value: Any, field: FieldSchema) -> Any:
        """타입 변환 & 검증"""
        
        # 타입 변환
        if field.data_type == DataType.STRING:
            value = str(value)
            
            # 길이 확인
            if field.min_length and len(value) < field.min_length:
                raise ValueError(f"Field '{field.name}' minimum length is {field.min_length}")
            if field.max_length and len(value) > field.max_length:
                raise ValueError(f"Field '{field.name}' maximum length is {field.max_length}")
            
            # 패턴 확인
            if field.pattern:
                import re
                if not re.match(field.pattern, value):
                    raise ValueError(f"Field '{field.name}' doesn't match pattern {field.pattern}")
        
        elif field.data_type == DataType.INTEGER:
            value = int(value)
            
            if field.min_value and value < field.min_value:
                raise ValueError(f"Field '{field.name}' must be >= {field.min_value}")
            if field.max_value and value > field.max_value:
                raise ValueError(f"Field '{field.name}' must be <= {field.max_value}")
        
        elif field.data_type == DataType.FLOAT:
            value = float(value)
            
            if field.min_value and value < field.min_value:
                raise ValueError(f"Field '{field.name}' must be >= {field.min_value}")
            if field.max_value and value > field.max_value:
                raise ValueError(f"Field '{field.name}' must be <= {field.max_value}")
        
        elif field.data_type == DataType.BOOLEAN:
            if isinstance(value, bool):
                pass
            elif isinstance(value, str):
                value = value.lower() in ['true', '1', 'yes']
            else:
                value = bool(value)
        
        elif field.data_type == DataType.ARRAY:
            if not isinstance(value, list):
                raise ValueError(f"Field '{field.name}' must be an array")
        
        elif field.data_type == DataType.OBJECT:
            if not isinstance(value, dict):
                raise ValueError(f"Field '{field.name}' must be an object")
        
        # 허용 값 확인
        if field.allowed_values and value not in field.allowed_values:
            raise ValueError(f"Field '{field.name}' must be one of {field.allowed_values}")
        
        return value


class DataTransformer:
    """데이터 변환"""
    
    def __init__(self):
        self.transformations: Dict[str, Callable] = {}
    
    def register_transformation(self, name: str, transformer: Callable):
        """변환 등록"""
        self.transformations[name] = transformer
    
    def transform(self, data: Dict[str, Any], transformation_name: str) -> Dict[str, Any]:
        """데이터 변환"""
        
        if transformation_name not in self.transformations:
            return {'status': 'error', 'message': f'Transformation {transformation_name} not found'}
        
        try:
            result = self.transformations[transformation_name](data)
            return {'status': 'success', 'data': result}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """정규화 (공백 제거, 소문자 변환)"""
        
        normalized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                normalized[key] = value.strip().lower()
            elif isinstance(value, dict):
                normalized[key] = self.normalize(value)
            else:
                normalized[key] = value
        
        return normalized
    
    def sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """살균 (위험한 문자 제거)"""
        
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # HTML/SQL 특수 문자 제거
                value = value.replace('<', '').replace('>', '')
                value = value.replace(';', '').replace("'", '')
                sanitized[key] = value
            else:
                sanitized[key] = value
        
        return sanitized


class ValidationPipeline:
    """검증 파이프라인"""
    
    def __init__(self):
        self.validator = SchemaValidator()
        self.transformer = DataTransformer()
    
    async def process(
        self,
        data: Dict[str, Any],
        schema_name: str,
        transformations: List[str] = None
    ) -> Dict[str, Any]:
        """데이터 처리 파이프라인"""
        
        from datetime import datetime
        
        start_time = datetime.now()
        
        # 1단계: 정규화
        normalized = self.transformer.normalize(data)
        
        # 2단계: 살균
        sanitized = self.transformer.sanitize(normalized)
        
        # 3단계: 검증
        validation_result = self.validator.validate(schema_name, sanitized)
        
        if not validation_result['valid']:
            return {
                'status': 'validation_failed',
                'errors': validation_result['errors']
            }
        
        processed_data = validation_result['data']
        
        # 4단계: 변환
        if transformations:
            for transform_name in transformations:
                transform_result = self.transformer.transform(processed_data, transform_name)
                if transform_result['status'] == 'success':
                    processed_data = transform_result['data']
                else:
                    return transform_result
        
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            'status': 'success',
            'data': processed_data,
            'duration_ms': duration_ms
        }


if __name__ == "__main__":
    print("✅ 데이터 검증 & 변환 테스트\n")
    
    pipeline = ValidationPipeline()
    
    # 스키마 정의
    user_schema = [
        FieldSchema('name', DataType.STRING, required=True, min_length=2, max_length=50),
        FieldSchema('email', DataType.STRING, required=True, pattern=r'^[\w.-]+@[\w.-]+\.\w+$'),
        FieldSchema('age', DataType.INTEGER, required=False, min_value=0, max_value=150),
        FieldSchema('role', DataType.STRING, required=False, allowed_values=['admin', 'user', 'guest']),
    ]
    
    pipeline.validator.register_schema('user', user_schema)
    
    print("✅ 스키마 등록 완료!")
    
    # 검증
    test_data = {
        'name': '  Alice  ',
        'email': 'alice@example.com',
        'age': '25',
        'role': 'admin'
    }
    
    import asyncio
    
    async def test():
        result = await pipeline.process(test_data, 'user')
        
        print(f"✅ 처리 완료!")
        print(f"상태: {result.get('status')}")
        
        if result.get('status') == 'success':
            print(f"데이터: {result.get('data')}")
            print(f"소요시간: {result.get('duration_ms'):.2f}ms")
        else:
            print(f"에러: {result.get('errors')}")
    
    asyncio.run(test())
