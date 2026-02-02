"""
에러 처리 & 복구 - 강건한 시스템

역할:
- 에러 분류 및 로깅
- 자동 복구 전략
- Graceful degradation
- 사용자 친화적 메시지
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    """에러 심각도"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """에러 카테고리"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    INTERNAL_SERVER = "internal_server"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TIMEOUT = "timeout"


@dataclass
class ErrorContext:
    """에러 컨텍스트"""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Dict[str, Any]
    timestamp: datetime = None
    source: str = None
    stack_trace: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ErrorClassifier:
    """에러 분류기"""
    
    def __init__(self):
        self.error_patterns = {
            'validation': ['invalid', 'required', 'format', 'type'],
            'authentication': ['unauthorized', 'not authenticated', 'invalid token'],
            'authorization': ['forbidden', 'permission denied', 'not allowed'],
            'not_found': ['not found', '404', 'missing'],
            'timeout': ['timeout', 'took too long'],
            'service': ['service unavailable', '503', 'temporarily unavailable']
        }
    
    def classify(self, error_message: str) -> ErrorCategory:
        """에러 분류"""
        
        message_lower = error_message.lower()
        
        for category, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    return ErrorCategory[category.upper()]
        
        return ErrorCategory.INTERNAL_SERVER
    
    def get_severity(self, category: ErrorCategory) -> ErrorSeverity:
        """심각도 결정"""
        
        severity_map = {
            ErrorCategory.VALIDATION: ErrorSeverity.WARNING,
            ErrorCategory.AUTHENTICATION: ErrorSeverity.ERROR,
            ErrorCategory.AUTHORIZATION: ErrorSeverity.WARNING,
            ErrorCategory.NOT_FOUND: ErrorSeverity.WARNING,
            ErrorCategory.CONFLICT: ErrorSeverity.WARNING,
            ErrorCategory.INTERNAL_SERVER: ErrorSeverity.CRITICAL,
            ErrorCategory.SERVICE_UNAVAILABLE: ErrorSeverity.CRITICAL,
            ErrorCategory.TIMEOUT: ErrorSeverity.ERROR
        }
        
        return severity_map.get(category, ErrorSeverity.ERROR)


class RecoveryStrategy:
    """복구 전략"""
    
    def __init__(self):
        self.recovery_handlers: Dict[ErrorCategory, Callable] = {}
        self.recovery_log = []
    
    def register_recovery(self, category: ErrorCategory, handler: Callable):
        """복구 핸들러 등록"""
        self.recovery_handlers[category] = handler
    
    async def recover(self, error_context: ErrorContext) -> Dict[str, Any]:
        """복구 시도"""
        
        recovery_start = datetime.now()
        
        handler = self.recovery_handlers.get(error_context.category)
        
        if not handler:
            return {
                'status': 'no_recovery_handler',
                'category': error_context.category.value
            }
        
        try:
            import asyncio
            
            if asyncio.iscoroutinefunction(handler):
                result = await handler(error_context)
            else:
                result = handler(error_context)
            
            recovery_duration_ms = (datetime.now() - recovery_start).total_seconds() * 1000
            
            recovery_result = {
                'status': 'recovered',
                'error_id': error_context.error_id,
                'category': error_context.category.value,
                'recovery_duration_ms': recovery_duration_ms,
                'result': result
            }
            
            self.recovery_log.append(recovery_result)
            
            return recovery_result
        
        except Exception as e:
            return {
                'status': 'recovery_failed',
                'error_id': error_context.error_id,
                'original_error': error_context.message,
                'recovery_error': str(e)
            }


class ErrorLogger:
    """에러 로거"""
    
    def __init__(self):
        self.error_log: List[ErrorContext] = []
        self.error_stats = {}
    
    def log_error(self, error_context: ErrorContext):
        """에러 로깅"""
        
        self.error_log.append(error_context)
        
        # 통계 업데이트
        category_key = error_context.category.value
        if category_key not in self.error_stats:
            self.error_stats[category_key] = {'count': 0, 'severity_distribution': {}}
        
        self.error_stats[category_key]['count'] += 1
        
        severity_key = error_context.severity.value
        if severity_key not in self.error_stats[category_key]['severity_distribution']:
            self.error_stats[category_key]['severity_distribution'][severity_key] = 0
        
        self.error_stats[category_key]['severity_distribution'][severity_key] += 1
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """최근 에러 조회"""
        
        return [
            {
                'error_id': e.error_id,
                'category': e.category.value,
                'severity': e.severity.value,
                'message': e.message,
                'timestamp': e.timestamp.isoformat()
            }
            for e in self.error_log[-limit:]
        ]
    
    def get_error_report(self) -> Dict[str, Any]:
        """에러 리포트"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_errors': len(self.error_log),
            'error_statistics': self.error_stats,
            'recent_errors': self.get_recent_errors(5)
        }


class GracefulDegradation:
    """Graceful Degradation"""
    
    def __init__(self):
        self.fallback_strategies: Dict[str, Callable] = {}
        self.degradation_mode = False
    
    def register_fallback(self, service_name: str, fallback_func: Callable):
        """대체 전략 등록"""
        self.fallback_strategies[service_name] = fallback_func
    
    async def get_response_with_fallback(
        self,
        primary_func: Callable,
        service_name: str
    ) -> Dict[str, Any]:
        """대체 전략을 사용한 응답"""
        
        try:
            import asyncio
            
            if asyncio.iscoroutinefunction(primary_func):
                result = await primary_func()
            else:
                result = primary_func()
            
            return {
                'status': 'success',
                'source': 'primary',
                'data': result
            }
        
        except Exception as e:
            # Primary 실패 시 fallback 시도
            fallback_func = self.fallback_strategies.get(service_name)
            
            if not fallback_func:
                return {
                    'status': 'error',
                    'message': str(e)
                }
            
            try:
                if asyncio.iscoroutinefunction(fallback_func):
                    result = await fallback_func()
                else:
                    result = fallback_func()
                
                self.degradation_mode = True
                
                return {
                    'status': 'degraded',
                    'source': 'fallback',
                    'data': result,
                    'warning': f'Using fallback due to: {str(e)}'
                }
            
            except Exception as fallback_error:
                return {
                    'status': 'error',
                    'primary_error': str(e),
                    'fallback_error': str(fallback_error)
                }


class ErrorHandler:
    """통합 에러 처리기"""
    
    def __init__(self):
        self.classifier = ErrorClassifier()
        self.recovery = RecoveryStrategy()
        self.logger = ErrorLogger()
        self.degradation = GracefulDegradation()
    
    async def handle_error(
        self,
        error: Exception,
        source: str = 'unknown'
    ) -> Dict[str, Any]:
        """에러 처리"""
        
        import uuid
        
        error_id = str(uuid.uuid4())[:8]
        error_message = str(error)
        
        # 에러 분류
        category = self.classifier.classify(error_message)
        severity = self.classifier.get_severity(category)
        
        # 에러 컨텍스트 생성
        error_context = ErrorContext(
            error_id=error_id,
            category=category,
            severity=severity,
            message=error_message,
            details={},
            source=source,
            stack_trace=None
        )
        
        # 로깅
        self.logger.log_error(error_context)
        
        # 복구 시도
        recovery_result = await self.recovery.recover(error_context)
        
        # 사용자 친화적 메시지
        user_message = self._get_user_friendly_message(category, error_message)
        
        return {
            'error_id': error_id,
            'category': category.value,
            'severity': severity.value,
            'user_message': user_message,
            'recovery_status': recovery_result.get('status'),
            'source': source,
            'timestamp': error_context.timestamp.isoformat()
        }
    
    def _get_user_friendly_message(self, category: ErrorCategory, detail: str) -> str:
        """사용자 친화적 메시지"""
        
        messages = {
            ErrorCategory.VALIDATION: "입력 데이터가 유효하지 않습니다. 다시 확인해주세요.",
            ErrorCategory.AUTHENTICATION: "인증이 필요합니다. 다시 로그인해주세요.",
            ErrorCategory.AUTHORIZATION: "이 작업을 수행할 권한이 없습니다.",
            ErrorCategory.NOT_FOUND: "요청한 리소스를 찾을 수 없습니다.",
            ErrorCategory.CONFLICT: "충돌이 발생했습니다. 다시 시도해주세요.",
            ErrorCategory.INTERNAL_SERVER: "서버에 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            ErrorCategory.SERVICE_UNAVAILABLE: "서비스가 일시적으로 이용 불가능합니다.",
            ErrorCategory.TIMEOUT: "요청 시간이 초과되었습니다. 다시 시도해주세요."
        }
        
        return messages.get(category, "오류가 발생했습니다.")
    
    def get_error_report(self) -> Dict[str, Any]:
        """에러 리포트"""
        return self.logger.get_error_report()


if __name__ == "__main__":
    print("🛡️ 에러 처리 & 복구 테스트\n")
    
    handler = ErrorHandler()
    
    # 복구 전략 등록
    async def validation_recovery(error_context):
        return {'strategy': 'default_values_applied'}
    
    handler.recovery.register_recovery(ErrorCategory.VALIDATION, validation_recovery)
    
    print("✅ 복구 전략 등록 완료!")
    
    # 에러 처리
    import asyncio
    
    async def test():
        try:
            raise ValueError("Username is required")
        except Exception as e:
            result = await handler.handle_error(e, source="user_registration")
            
            print("✅ 에러 처리 완료!")
            print(f"에러 ID: {result['error_id']}")
            print(f"사용자 메시지: {result['user_message']}")
            print(f"복구 상태: {result['recovery_status']}")
        
        # 리포트
        report = handler.get_error_report()
        print(f"\n✅ 에러 리포트:")
        print(f"총 에러: {report['total_errors']}")
    
    asyncio.run(test())
