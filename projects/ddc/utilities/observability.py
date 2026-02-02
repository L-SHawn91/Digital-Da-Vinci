"""
로깅 & 추적 - 시스템 관찰성

역할:
- 구조화된 로깅
- 분산 추적
- 성능 프로파일링
- 감사 추적
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """로그 레벨"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@dataclass
class LogEntry:
    """로그 항목"""
    timestamp: datetime
    level: LogLevel
    message: str
    context: Dict[str, Any]
    trace_id: str = None
    span_id: str = None
    duration_ms: float = None


class StructuredLogger:
    """구조화된 로거"""
    
    def __init__(self):
        self.logs: List[LogEntry] = []
        self.max_logs = 100000
    
    def log(
        self,
        level: LogLevel,
        message: str,
        context: Dict[str, Any] = None,
        trace_id: str = None
    ):
        """로깅"""
        
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            message=message,
            context=context or {},
            trace_id=trace_id
        )
        
        self.logs.append(entry)
        
        # 용량 초과 시 오래된 항목 제거
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
    
    def debug(self, message: str, context: Dict = None, trace_id: str = None):
        """DEBUG 로그"""
        self.log(LogLevel.DEBUG, message, context, trace_id)
    
    def info(self, message: str, context: Dict = None, trace_id: str = None):
        """INFO 로그"""
        self.log(LogLevel.INFO, message, context, trace_id)
    
    def warning(self, message: str, context: Dict = None, trace_id: str = None):
        """WARNING 로그"""
        self.log(LogLevel.WARNING, message, context, trace_id)
    
    def error(self, message: str, context: Dict = None, trace_id: str = None):
        """ERROR 로그"""
        self.log(LogLevel.ERROR, message, context, trace_id)
    
    def critical(self, message: str, context: Dict = None, trace_id: str = None):
        """CRITICAL 로그"""
        self.log(LogLevel.CRITICAL, message, context, trace_id)
    
    def get_logs_by_level(self, level: LogLevel) -> List[LogEntry]:
        """레벨별 로그 조회"""
        return [log for log in self.logs if log.level == level]
    
    def get_logs_by_trace(self, trace_id: str) -> List[LogEntry]:
        """추적 ID로 로그 조회"""
        return [log for log in self.logs if log.trace_id == trace_id]


class DistributedTracer:
    """분산 추적"""
    
    def __init__(self):
        self.traces: Dict[str, Dict[str, Any]] = {}
        self.spans: Dict[str, List[Dict[str, Any]]] = {}
    
    def create_trace(self, trace_id: str, service_name: str) -> Dict[str, Any]:
        """추적 생성"""
        
        self.traces[trace_id] = {
            'trace_id': trace_id,
            'service': service_name,
            'start_time': datetime.now(),
            'spans': []
        }
        
        self.spans[trace_id] = []
        
        return self.traces[trace_id]
    
    def add_span(
        self,
        trace_id: str,
        span_id: str,
        operation: str,
        start_time: datetime = None,
        duration_ms: float = None
    ):
        """스팬 추가"""
        
        if trace_id not in self.traces:
            return
        
        span = {
            'span_id': span_id,
            'operation': operation,
            'start_time': start_time or datetime.now(),
            'duration_ms': duration_ms or 0
        }
        
        self.spans[trace_id].append(span)
        self.traces[trace_id]['spans'].append(span_id)
    
    def get_trace_report(self, trace_id: str) -> Dict[str, Any]:
        """추적 리포트"""
        
        if trace_id not in self.traces:
            return {'status': 'trace_not_found'}
        
        trace = self.traces[trace_id]
        spans = self.spans.get(trace_id, [])
        
        total_duration_ms = sum(s.get('duration_ms', 0) for s in spans)
        
        return {
            'trace_id': trace_id,
            'service': trace['service'],
            'start_time': trace['start_time'].isoformat(),
            'span_count': len(spans),
            'total_duration_ms': total_duration_ms,
            'spans': spans
        }


class PerformanceProfiler:
    """성능 프로파일러"""
    
    def __init__(self):
        self.profiles: Dict[str, List[float]] = {}
        self.current_profiling = None
    
    def start_profiling(self, operation_name: str) -> str:
        """프로파일링 시작"""
        
        import uuid
        profile_id = str(uuid.uuid4())[:8]
        
        self.current_profiling = {
            'profile_id': profile_id,
            'operation': operation_name,
            'start_time': datetime.now()
        }
        
        return profile_id
    
    def end_profiling(self, profile_id: str) -> Dict[str, Any]:
        """프로파일링 종료"""
        
        if not self.current_profiling or self.current_profiling['profile_id'] != profile_id:
            return {'status': 'profile_not_found'}
        
        duration_ms = (datetime.now() - self.current_profiling['start_time']).total_seconds() * 1000
        operation = self.current_profiling['operation']
        
        if operation not in self.profiles:
            self.profiles[operation] = []
        
        self.profiles[operation].append(duration_ms)
        
        self.current_profiling = None
        
        return {
            'profile_id': profile_id,
            'operation': operation,
            'duration_ms': duration_ms
        }
    
    def get_profile_statistics(self, operation: str) -> Dict[str, Any]:
        """프로파일 통계"""
        
        if operation not in self.profiles:
            return {'status': 'no_profile_data'}
        
        durations = self.profiles[operation]
        
        import statistics
        
        return {
            'operation': operation,
            'samples': len(durations),
            'min_ms': min(durations),
            'max_ms': max(durations),
            'avg_ms': statistics.mean(durations),
            'median_ms': statistics.median(durations),
            'stdev_ms': statistics.stdev(durations) if len(durations) > 1 else 0
        }


class AuditLogger:
    """감사 로거"""
    
    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []
    
    def log_action(
        self,
        user_id: str,
        action: str,
        resource: str,
        result: str,
        details: Dict = None
    ):
        """액션 기록"""
        
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'result': result,
            'details': details or {}
        }
        
        self.audit_log.append(audit_entry)
    
    def get_audit_trail(
        self,
        user_id: str = None,
        action: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """감사 추적 조회"""
        
        filtered = self.audit_log
        
        if user_id:
            filtered = [e for e in filtered if e['user_id'] == user_id]
        
        if action:
            filtered = [e for e in filtered if e['action'] == action]
        
        return filtered[-limit:]


class ObservabilityPlatform:
    """관찰성 플랫폼"""
    
    def __init__(self):
        self.logger = StructuredLogger()
        self.tracer = DistributedTracer()
        self.profiler = PerformanceProfiler()
        self.auditor = AuditLogger()
    
    async def trace_operation(
        self,
        operation_name: str,
        operation_func: Callable,
        user_id: str = None
    ) -> Dict[str, Any]:
        """작업 추적"""
        
        import uuid
        import asyncio
        
        trace_id = str(uuid.uuid4())[:16]
        
        # 추적 생성
        self.tracer.create_trace(trace_id, 'system')
        
        # 프로파일링 시작
        profile_id = self.profiler.start_profiling(operation_name)
        
        # 로깅
        self.logger.info(f"Starting operation: {operation_name}", trace_id=trace_id)
        
        try:
            # 작업 실행
            if asyncio.iscoroutinefunction(operation_func):
                result = await operation_func()
            else:
                result = operation_func()
            
            # 프로파일링 종료
            profile_result = self.profiler.end_profiling(profile_id)
            
            # 스팬 추가
            self.tracer.add_span(
                trace_id,
                profile_id,
                operation_name,
                duration_ms=profile_result['duration_ms']
            )
            
            # 감사 로깅
            if user_id:
                self.auditor.log_action(
                    user_id,
                    operation_name,
                    'system',
                    'success'
                )
            
            self.logger.info(f"Completed operation: {operation_name}", trace_id=trace_id)
            
            return {
                'status': 'success',
                'trace_id': trace_id,
                'duration_ms': profile_result['duration_ms'],
                'result': result
            }
        
        except Exception as e:
            self.logger.error(f"Failed operation: {operation_name}", context={'error': str(e)}, trace_id=trace_id)
            
            if user_id:
                self.auditor.log_action(
                    user_id,
                    operation_name,
                    'system',
                    'failed',
                    {'error': str(e)}
                )
            
            return {
                'status': 'error',
                'trace_id': trace_id,
                'message': str(e)
            }
    
    def get_observability_report(self) -> Dict[str, Any]:
        """관찰성 리포트"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_logs': len(self.logger.logs),
            'total_traces': len(self.tracer.traces),
            'total_audit_entries': len(self.auditor.audit_log),
            'profiled_operations': list(self.profiler.profiles.keys()),
            'recent_logs': [
                {
                    'level': log.level.name,
                    'message': log.message,
                    'timestamp': log.timestamp.isoformat()
                }
                for log in self.logger.logs[-10:]
            ]
        }


if __name__ == "__main__":
    print("📊 로깅 & 추적 테스트\n")
    
    platform = ObservabilityPlatform()
    
    async def test_operation():
        import asyncio
        await asyncio.sleep(0.1)
        return {'data': 'test_result'}
    
    import asyncio
    
    async def test():
        result = await platform.trace_operation(
            'test_operation',
            test_operation,
            user_id='user_123'
        )
        
        print(f"✅ 작업 완료!")
        print(f"상태: {result['status']}")
        print(f"추적 ID: {result['trace_id']}")
        print(f"소요시간: {result['duration_ms']:.1f}ms")
        
        report = platform.get_observability_report()
        print(f"\n✅ 관찰성 리포트:")
        print(f"로그: {report['total_logs']}")
        print(f"추적: {report['total_traces']}")
        print(f"감사: {report['total_audit_entries']}")
    
    asyncio.run(test())
