"""
Circuit Breaker - 서킷 브레이커 패턴으로 장애 전파 방지

모델 장애를 감지하고 자동으로 격리하여 연쇄 장애를 방지합니다.
"""

import json
import time
from typing import Dict, Optional, Callable, Any
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict


class CircuitState(Enum):
    """서킷 상태"""
    CLOSED = "closed"          # 정상, 요청 허용
    OPEN = "open"              # 장애, 요청 차단
    HALF_OPEN = "half_open"    # 복구 시도, 제한적 요청


@dataclass
class CircuitEvent:
    """서킷 이벤트"""
    timestamp: float
    model: str
    state: str
    reason: str
    details: Dict = None


class CircuitBreaker:
    """서킷 브레이커"""
    
    def __init__(
        self,
        model: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_max_calls: int = 3
    ):
        """
        초기화
        
        Args:
            model: 모델명
            failure_threshold: 실패 임계값 (연속 실패 횟수)
            recovery_timeout: 복구 시간 초과 (초)
            half_open_max_calls: Half-Open 상태에서 허용할 최대 호출
        """
        self.model = model
        self.state = CircuitState.CLOSED
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state_change_time = time.time()
        
        self.metrics = {
            'total_calls': 0,
            'total_failures': 0,
            'total_successes': 0,
            'rejected_calls': 0
        }
        
        self.events: list[CircuitEvent] = []
    
    def call(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        서킷 브레이커를 통한 함수 호출
        
        Args:
            func: 호출할 함수
            *args: 위치 인수
            **kwargs: 키워드 인수
            
        Returns:
            함수 반환값
            
        Raises:
            Exception: 서킷이 OPEN 상태이거나 함수 실행 실패
        """
        self._check_state_transition()
        
        if self.state == CircuitState.OPEN:
            self._record_rejection()
            raise Exception(f"Circuit breaker OPEN for {self.model}")
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise
    
    def _check_state_transition(self) -> None:
        """상태 전환 확인"""
        if self.state == CircuitState.OPEN:
            # Open → Half-Open 전환 확인
            elapsed = time.time() - self.state_change_time
            if elapsed >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN, "Recovery timeout reached")
        
        elif self.state == CircuitState.HALF_OPEN:
            # Half-Open에서 충분히 성공했으면 Closed로 전환
            if self.success_count >= self.half_open_max_calls:
                self._transition_to(CircuitState.CLOSED, "Recovered successfully")
    
    def record_success(self) -> None:
        """성공 기록"""
        self.metrics['total_calls'] += 1
        self.metrics['total_successes'] += 1
        self.failure_count = 0
        self.success_count += 1
        
        # Half-Open 상태에서 충분한 성공 시 Closed로 복구
        if self.state == CircuitState.HALF_OPEN and \
           self.success_count >= self.half_open_max_calls:
            self._transition_to(CircuitState.CLOSED, "Recovered")
    
    def record_failure(self, reason: str = "Unknown") -> None:
        """실패 기록"""
        self.metrics['total_calls'] += 1
        self.metrics['total_failures'] += 1
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        # 실패 임계값 도달 시 Open으로 전환
        if self.failure_count >= self.failure_threshold:
            self._transition_to(CircuitState.OPEN, f"Failure threshold reached: {reason}")
    
    def _transition_to(self, new_state: CircuitState, reason: str) -> None:
        """상태 전환"""
        old_state = self.state
        self.state = new_state
        self.state_change_time = time.time()
        
        # Half-Open 상태로 전환할 때 카운터 리셋
        if new_state == CircuitState.HALF_OPEN:
            self.success_count = 0
            self.failure_count = 0
        
        # 복구 완료 시 카운터 리셋
        if new_state == CircuitState.CLOSED:
            self.success_count = 0
            self.failure_count = 0
        
        event = CircuitEvent(
            timestamp=time.time(),
            model=self.model,
            state=new_state.value,
            reason=reason,
            details={
                'from_state': old_state.value,
                'failure_count': self.failure_count,
                'success_count': self.success_count
            }
        )
        self.events.append(event)
    
    def _record_rejection(self) -> None:
        """거부 기록"""
        self.metrics['total_calls'] += 1
        self.metrics['rejected_calls'] += 1
    
    def get_status(self) -> Dict:
        """상태 조회"""
        return {
            'model': self.model,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'state_duration_sec': time.time() - self.state_change_time,
            'last_failure': datetime.fromtimestamp(self.last_failure_time).isoformat()
                          if self.last_failure_time else None,
            'metrics': self.metrics,
            'success_rate': self._calculate_success_rate()
        }
    
    def _calculate_success_rate(self) -> str:
        """성공률 계산"""
        total = self.metrics['total_calls']
        if total == 0:
            return "0%"
        
        success_rate = (self.metrics['total_successes'] / total) * 100
        return f"{success_rate:.1f}%"
    
    def reset(self) -> None:
        """서킷 초기화"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state_change_time = time.time()
        
        event = CircuitEvent(
            timestamp=time.time(),
            model=self.model,
            state=self.state.value,
            reason="Manual reset",
            details={}
        )
        self.events.append(event)


class CircuitBreakerManager:
    """서킷 브레이커 관리자"""
    
    def __init__(self):
        """초기화"""
        self.breakers: Dict[str, CircuitBreaker] = {}
    
    def get_breaker(self, model: str) -> CircuitBreaker:
        """서킷 브레이커 가져오기 또는 생성"""
        if model not in self.breakers:
            self.breakers[model] = CircuitBreaker(model)
        
        return self.breakers[model]
    
    def call_with_circuit_breaker(
        self,
        model: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        서킷 브레이커를 통한 함수 호출
        
        Args:
            model: 모델명
            func: 호출할 함수
            *args: 위치 인수
            **kwargs: 키워드 인수
            
        Returns:
            함수 반환값
        """
        breaker = self.get_breaker(model)
        return breaker.call(func, *args, **kwargs)
    
    def get_all_status(self) -> Dict[str, Dict]:
        """모든 서킷 상태 조회"""
        return {
            model: breaker.get_status()
            for model, breaker in self.breakers.items()
        }
    
    def get_open_circuits(self) -> list[str]:
        """OPEN 상태인 서킷 목록"""
        return [
            model for model, breaker in self.breakers.items()
            if breaker.state == CircuitState.OPEN
        ]
    
    def get_half_open_circuits(self) -> list[str]:
        """HALF_OPEN 상태인 서킷 목록"""
        return [
            model for model, breaker in self.breakers.items()
            if breaker.state == CircuitState.HALF_OPEN
        ]
    
    def reset_circuit(self, model: str) -> None:
        """특정 서킷 리셋"""
        if model in self.breakers:
            self.breakers[model].reset()
    
    def reset_all_circuits(self) -> None:
        """모든 서킷 리셋"""
        for breaker in self.breakers.values():
            breaker.reset()
    
    def get_circuit_report(self) -> Dict:
        """서킷 브레이커 리포트"""
        all_status = self.get_all_status()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_circuits': len(self.breakers),
            'open_count': len(self.get_open_circuits()),
            'half_open_count': len(self.get_half_open_circuits()),
            'closed_count': sum(
                1 for s in all_status.values()
                if s['state'] == 'closed'
            ),
            'details': all_status
        }
    
    def export_report(self, filename: str) -> None:
        """리포트 내보내기"""
        report = self.get_circuit_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)


# 테스트 코드
if __name__ == "__main__":
    manager = CircuitBreakerManager()
    
    # 테스트 함수
    def failing_function():
        raise Exception("Model failure")
    
    def success_function():
        return "Success"
    
    breaker = manager.get_breaker("TestModel")
    
    # 실패 시뮬레이션
    print("=== Failure Simulation ===")
    for i in range(6):
        try:
            manager.call_with_circuit_breaker("TestModel", failing_function)
        except Exception as e:
            print(f"Call {i+1}: {e}")
            breaker.record_failure("Test failure")
        
        status = breaker.get_status()
        print(f"State: {status['state']}, Failures: {status['failure_count']}")
    
    print("\n=== Circuit Status ===")
    report = manager.get_circuit_report()
    print(json.dumps(report, indent=2, default=str))
