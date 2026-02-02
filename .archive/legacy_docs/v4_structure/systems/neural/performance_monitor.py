"""
Performance Monitor - 신경계 실시간 성능 모니터링

L1-L4 신경계별 성능을 실시간으로 추적하고 이상을 감지합니다.
"""

import json
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum


class PerformanceLevel(Enum):
    """성능 레벨 정의"""
    EXCELLENT = "excellent"  # > 95%
    GOOD = "good"            # 85-95%
    NORMAL = "normal"        # 70-85%
    POOR = "poor"            # 50-70%
    CRITICAL = "critical"    # < 50%


@dataclass
class PerformanceMetric:
    """성능 메트릭 단위"""
    timestamp: float
    response_time_ms: float
    tokens_used: int
    success: bool
    model: str
    neural_level: str


@dataclass
class NeuralLevelStats:
    """신경계 레벨 통계"""
    level: str  # L1, L2, L3, L4
    total_calls: int = 0
    success_count: int = 0
    avg_response_time: float = 0.0
    total_tokens: int = 0
    performance_level: PerformanceLevel = PerformanceLevel.NORMAL
    last_updated: float = field(default_factory=time.time)
    
    @property
    def success_rate(self) -> float:
        """성공률 계산"""
        if self.total_calls == 0:
            return 0.0
        return (self.success_count / self.total_calls) * 100


class PerformanceMonitor:
    """신경계 성능 모니터링 시스템"""
    
    def __init__(self, history_size: int = 1000):
        """
        초기화
        
        Args:
            history_size: 유지할 최대 히스토리 수
        """
        self.history_size = history_size
        self.metrics_history: List[PerformanceMetric] = []
        self.neural_stats: Dict[str, NeuralLevelStats] = {
            'L1': NeuralLevelStats('L1'),
            'L2': NeuralLevelStats('L2'),
            'L3': NeuralLevelStats('L3'),
            'L4': NeuralLevelStats('L4'),
        }
        self.anomalies: List[Dict] = []
        self.thresholds = {
            'response_time': 5000,      # ms
            'success_rate': 80.0,        # %
            'token_per_call': 1000,      # tokens
        }
    
    def record_execution(
        self,
        response_time_ms: float,
        tokens_used: int,
        success: bool,
        model: str,
        neural_level: str
    ) -> None:
        """
        작업 실행 기록
        
        Args:
            response_time_ms: 응답 시간 (밀리초)
            tokens_used: 토큰 사용량
            success: 성공 여부
            model: 사용 모델
            neural_level: 신경계 레벨 (L1-L4)
        """
        metric = PerformanceMetric(
            timestamp=time.time(),
            response_time_ms=response_time_ms,
            tokens_used=tokens_used,
            success=success,
            model=model,
            neural_level=neural_level
        )
        
        # 히스토리에 추가
        self.metrics_history.append(metric)
        if len(self.metrics_history) > self.history_size:
            self.metrics_history.pop(0)
        
        # 통계 업데이트
        self._update_neural_stats(metric)
        
        # 이상 감지
        self._detect_anomalies(metric)
    
    def _update_neural_stats(self, metric: PerformanceMetric) -> None:
        """신경계 통계 업데이트"""
        stats = self.neural_stats[metric.neural_level]
        stats.total_calls += 1
        
        if metric.success:
            stats.success_count += 1
        
        # 평균 응답시간 업데이트
        old_avg = stats.avg_response_time
        stats.avg_response_time = (
            (old_avg * (stats.total_calls - 1) + metric.response_time_ms) /
            stats.total_calls
        )
        
        # 총 토큰 업데이트
        stats.total_tokens += metric.tokens_used
        
        # 성능 레벨 결정
        success_rate = stats.success_rate
        if success_rate > 95:
            stats.performance_level = PerformanceLevel.EXCELLENT
        elif success_rate > 85:
            stats.performance_level = PerformanceLevel.GOOD
        elif success_rate > 70:
            stats.performance_level = PerformanceLevel.NORMAL
        elif success_rate > 50:
            stats.performance_level = PerformanceLevel.POOR
        else:
            stats.performance_level = PerformanceLevel.CRITICAL
        
        stats.last_updated = time.time()
    
    def _detect_anomalies(self, metric: PerformanceMetric) -> None:
        """이상 탐지"""
        anomalies = []
        
        # 응답시간 이상
        if metric.response_time_ms > self.thresholds['response_time']:
            anomalies.append({
                'type': 'slow_response',
                'value': metric.response_time_ms,
                'threshold': self.thresholds['response_time'],
                'model': metric.model,
                'level': metric.neural_level
            })
        
        # 토큰 사용량 이상
        if metric.tokens_used > self.thresholds['token_per_call']:
            anomalies.append({
                'type': 'high_token_usage',
                'value': metric.tokens_used,
                'threshold': self.thresholds['token_per_call'],
                'model': metric.model,
                'level': metric.neural_level
            })
        
        # 신경계별 성공률 이상
        stats = self.neural_stats[metric.neural_level]
        if stats.success_rate < self.thresholds['success_rate']:
            anomalies.append({
                'type': 'low_success_rate',
                'value': stats.success_rate,
                'threshold': self.thresholds['success_rate'],
                'level': metric.neural_level
            })
        
        # 이상 기록
        for anomaly in anomalies:
            anomaly['timestamp'] = time.time()
            self.anomalies.append(anomaly)
            if len(self.anomalies) > self.history_size:
                self.anomalies.pop(0)
    
    def get_neural_health_status(self) -> Dict[str, Dict]:
        """신경계 전체 상태 반환"""
        status = {}
        for level, stats in self.neural_stats.items():
            status[level] = {
                'level': stats.level,
                'total_calls': stats.total_calls,
                'success_count': stats.success_count,
                'success_rate': f"{stats.success_rate:.1f}%",
                'avg_response_time': f"{stats.avg_response_time:.1f}ms",
                'total_tokens': stats.total_tokens,
                'performance_level': stats.performance_level.value,
                'last_updated': datetime.fromtimestamp(stats.last_updated).isoformat()
            }
        return status
    
    def get_model_health_status(self) -> Dict[str, Dict]:
        """모델별 상태 반환"""
        model_stats: Dict[str, Dict] = {}
        
        for metric in self.metrics_history:
            if metric.model not in model_stats:
                model_stats[metric.model] = {
                    'total_calls': 0,
                    'success_count': 0,
                    'total_tokens': 0,
                    'response_times': []
                }
            
            stats = model_stats[metric.model]
            stats['total_calls'] += 1
            if metric.success:
                stats['success_count'] += 1
            stats['total_tokens'] += metric.tokens_used
            stats['response_times'].append(metric.response_time_ms)
        
        # 통계 계산
        result = {}
        for model, stats in model_stats.items():
            success_rate = (stats['success_count'] / stats['total_calls'] * 100
                          if stats['total_calls'] > 0 else 0)
            avg_response = (sum(stats['response_times']) / len(stats['response_times'])
                          if stats['response_times'] else 0)
            
            result[model] = {
                'total_calls': stats['total_calls'],
                'success_rate': f"{success_rate:.1f}%",
                'avg_response_time': f"{avg_response:.1f}ms",
                'total_tokens': stats['total_tokens'],
                'tokens_per_call': f"{stats['total_tokens'] / stats['total_calls']:.0f}"
            }
        
        return result
    
    def detect_anomalies(self) -> List[Dict]:
        """최근 이상 탐지 반환"""
        return self.anomalies[-10:]  # 최근 10개
    
    def get_performance_report(self) -> Dict:
        """성능 리포트 생성"""
        return {
            'timestamp': datetime.now().isoformat(),
            'neural_health': self.get_neural_health_status(),
            'model_health': self.get_model_health_status(),
            'recent_anomalies': self.detect_anomalies(),
            'history_size': len(self.metrics_history),
            'anomaly_count': len(self.anomalies)
        }
    
    def set_threshold(self, threshold_type: str, value: float) -> None:
        """임계값 설정"""
        if threshold_type in self.thresholds:
            self.thresholds[threshold_type] = value
    
    def export_metrics(self, filename: str) -> None:
        """메트릭을 파일로 내보내기"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'metrics': [asdict(m) for m in self.metrics_history],
            'anomalies': self.anomalies,
            'neural_stats': {
                level: asdict(stats)
                for level, stats in self.neural_stats.items()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)


# 테스트 코드
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # 샘플 데이터 기록
    monitor.record_execution(1200, 500, True, "Gemini", "L1")
    monitor.record_execution(1500, 600, True, "Claude", "L2")
    monitor.record_execution(8000, 1500, False, "Groq", "L3")  # 이상
    monitor.record_execution(900, 400, True, "DeepSeek", "L4")
    
    # 성능 리포트 출력
    report = monitor.get_performance_report()
    print(json.dumps(report, indent=2, default=str))
