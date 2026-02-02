"""
Fallback Manager - 토큰 부족/모델 실패 시 자동 폴백

모델 토큰 사용량을 추적하고, 부족하거나 실패할 때 자동으로 대체 모델로 전환합니다.
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict


class FallbackReason(Enum):
    """폴백 사유"""
    TOKEN_EXHAUSTED = "token_exhausted"
    MODEL_FAILURE = "model_failure"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    HIGH_LATENCY = "high_latency"


@dataclass
class FallbackEvent:
    """폴백 이벤트"""
    timestamp: float
    reason: str
    from_model: str
    to_model: str
    neural_level: str
    success: bool


class FallbackManager:
    """폴백 관리자"""
    
    def __init__(self):
        """초기화"""
        self.model_tokens: Dict[str, Dict] = {}
        self.model_status: Dict[str, str] = {}
        self.fallback_history: List[FallbackEvent] = []
        self.fallback_policies: Dict[str, List[str]] = {}
        
        # 신경계별 폴백 정책 (우선순위 순서)
        self.fallback_policies = {
            'L1': ['Groq', 'DeepSeek', 'OpenAI', 'Gemini'],
            'L2': ['Gemini', 'Claude', 'DeepSeek', 'OpenAI'],
            'L3': ['Claude', 'Gemini', 'Mistral', 'DeepSeek'],
            'L4': ['DeepSeek', 'Gemini', 'Claude', 'OpenAI'],
        }
        
        # 모델별 토큰 한도 (일일)
        self.token_limits = {
            'Gemini': 1_000_000,
            'Claude': 800_000,
            'Groq': 500_000,
            'DeepSeek': 600_000,
            'OpenAI': 700_000,
            'Mistral': 400_000,
            'SambaNova': 300_000,
            'Cerebras': 250_000,
        }
        
        # 토큰 리셋 시간 (UTC 시간)
        self.reset_hour = 0
        
        self._initialize_model_tokens()
    
    def _initialize_model_tokens(self) -> None:
        """모델 토큰 초기화"""
        for model, limit in self.token_limits.items():
            self.model_tokens[model] = {
                'limit': limit,
                'used': 0,
                'available': limit,
                'last_reset': time.time(),
                'reset_time': self._get_next_reset_time()
            }
            self.model_status[model] = 'healthy'
    
    def _get_next_reset_time(self) -> float:
        """다음 리셋 시간 계산"""
        now = datetime.now()
        next_reset = now.replace(hour=self.reset_hour, minute=0, second=0, microsecond=0)
        
        if next_reset <= now:
            next_reset += timedelta(days=1)
        
        return next_reset.timestamp()
    
    def check_token_availability(self, model: str, tokens_needed: int) -> Tuple[bool, str]:
        """
        토큰 가용성 확인
        
        Args:
            model: 모델명
            tokens_needed: 필요한 토큰 수
            
        Returns:
            (가용 여부, 상태 메시지)
        """
        if model not in self.model_tokens:
            return False, f"Unknown model: {model}"
        
        # 토큰 리셋 확인
        self._check_and_reset_tokens(model)
        
        tokens = self.model_tokens[model]
        available = tokens['available']
        
        if available < tokens_needed:
            usage_percent = (tokens['used'] / tokens['limit']) * 100
            return False, f"Insufficient tokens: {available}/{tokens_needed} (Usage: {usage_percent:.1f}%)"
        
        return True, "Tokens available"
    
    def _check_and_reset_tokens(self, model: str) -> None:
        """토큰 리셋 확인 및 실행"""
        tokens = self.model_tokens[model]
        
        if time.time() >= tokens['reset_time']:
            tokens['used'] = 0
            tokens['available'] = tokens['limit']
            tokens['last_reset'] = time.time()
            tokens['reset_time'] = self._get_next_reset_time()
            self.model_status[model] = 'healthy'
    
    def consume_tokens(self, model: str, tokens_used: int) -> bool:
        """
        토큰 소비 기록
        
        Args:
            model: 모델명
            tokens_used: 소비한 토큰 수
            
        Returns:
            성공 여부
        """
        if model not in self.model_tokens:
            return False
        
        self._check_and_reset_tokens(model)
        
        tokens = self.model_tokens[model]
        tokens['used'] += tokens_used
        tokens['available'] = max(0, tokens['limit'] - tokens['used'])
        
        # 임계값 체크
        usage_percent = (tokens['used'] / tokens['limit']) * 100
        if usage_percent >= 90:
            self.model_status[model] = 'warning'
        if usage_percent >= 100:
            self.model_status[model] = 'exhausted'
        
        return True
    
    def record_model_failure(self, model: str, error: str) -> None:
        """
        모델 실패 기록
        
        Args:
            model: 모델명
            error: 에러 메시지
        """
        self.model_status[model] = 'failure'
    
    def trigger_fallback(
        self,
        current_model: str,
        neural_level: str,
        reason: FallbackReason
    ) -> Optional[str]:
        """
        폴백 실행
        
        Args:
            current_model: 현재 모델
            neural_level: 신경계 레벨
            reason: 폴백 사유
            
        Returns:
            폴백할 모델명 (없으면 None)
        """
        fallback_candidates = self.fallback_policies.get(neural_level, [])
        
        for fallback_model in fallback_candidates:
            if fallback_model == current_model:
                continue
            
            # 해당 모델 건강 상태 확인
            if self.model_status.get(fallback_model) == 'exhausted':
                continue
            
            # 토큰 가용성 확인
            available, _ = self.check_token_availability(fallback_model, 100)
            if not available:
                continue
            
            # 폴백 성공
            event = FallbackEvent(
                timestamp=time.time(),
                reason=reason.value,
                from_model=current_model,
                to_model=fallback_model,
                neural_level=neural_level,
                success=True
            )
            self.fallback_history.append(event)
            
            return fallback_model
        
        # 폴백 실패
        event = FallbackEvent(
            timestamp=time.time(),
            reason=reason.value,
            from_model=current_model,
            to_model='none',
            neural_level=neural_level,
            success=False
        )
        self.fallback_history.append(event)
        
        return None
    
    def get_fallback_model(
        self,
        current_model: str,
        neural_level: str
    ) -> Optional[str]:
        """
        다음 폴백 모델 선택
        
        Args:
            current_model: 현재 모델
            neural_level: 신경계 레벨
            
        Returns:
            폴백 모델명
        """
        candidates = self.fallback_policies.get(neural_level, [])
        
        for model in candidates:
            if model == current_model:
                continue
            
            status = self.model_status.get(model, 'unknown')
            if status in ['failure', 'exhausted']:
                continue
            
            return model
        
        return None
    
    def get_model_status(self) -> Dict[str, Dict]:
        """모델 상태 조회"""
        status = {}
        
        for model, tokens in self.model_tokens.items():
            self._check_and_reset_tokens(model)
            
            usage_percent = (tokens['used'] / tokens['limit']) * 100
            status[model] = {
                'status': self.model_status.get(model, 'unknown'),
                'tokens_used': tokens['used'],
                'tokens_available': tokens['available'],
                'tokens_limit': tokens['limit'],
                'usage_percent': f"{usage_percent:.1f}%",
                'last_reset': datetime.fromtimestamp(tokens['last_reset']).isoformat(),
                'next_reset': datetime.fromtimestamp(tokens['reset_time']).isoformat()
            }
        
        return status
    
    def log_fallback_event(self, event: FallbackEvent) -> None:
        """폴백 이벤트 로깅"""
        if len(self.fallback_history) > 1000:
            self.fallback_history.pop(0)
    
    def get_fallback_statistics(self) -> Dict:
        """폴백 통계"""
        total = len(self.fallback_history)
        successful = sum(1 for e in self.fallback_history if e.success)
        failed = total - successful
        
        reason_count = {}
        for event in self.fallback_history:
            reason = event.reason
            reason_count[reason] = reason_count.get(reason, 0) + 1
        
        model_transitions = {}
        for event in self.fallback_history:
            key = f"{event.from_model} → {event.to_model}"
            model_transitions[key] = model_transitions.get(key, 0) + 1
        
        return {
            'total_fallbacks': total,
            'successful_fallbacks': successful,
            'failed_fallbacks': failed,
            'success_rate': f"{(successful / max(1, total)) * 100:.1f}%",
            'reasons': reason_count,
            'model_transitions': model_transitions,
            'recent_events': [asdict(e) for e in self.fallback_history[-10:]]
        }
    
    def export_fallback_log(self, filename: str) -> None:
        """폴백 로그 내보내기"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'model_status': self.get_model_status(),
            'fallback_statistics': self.get_fallback_statistics(),
            'fallback_history': [asdict(e) for e in self.fallback_history]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)


# 테스트 코드
if __name__ == "__main__":
    manager = FallbackManager()
    
    # 토큰 소비
    manager.consume_tokens('Gemini', 100)
    manager.consume_tokens('Claude', 200)
    
    # 가용성 확인
    available, msg = manager.check_token_availability('Gemini', 50)
    print(f"Gemini: {available}, {msg}")
    
    # 폴백 시뮬레이션
    fallback_model = manager.trigger_fallback('Gemini', 'L1', FallbackReason.TOKEN_EXHAUSTED)
    print(f"Fallback: Gemini → {fallback_model}")
    
    # 통계
    stats = manager.get_fallback_statistics()
    print(json.dumps(stats, indent=2, default=str))
